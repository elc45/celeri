import importlib.util
from typing import TYPE_CHECKING, Literal

import numpy as np
import pandas as pd
from loguru import logger
from scipy import linalg, spatial

from celeri.constants import RADIUS_EARTH
from celeri.model import Model
from celeri.operators import Operators, build_operators
from celeri.solve import Estimation, build_estimation

if TYPE_CHECKING or importlib.util.find_spec("pymc") is None:
    # Fallback for PyMC if not installed
    # This is a minimal stub for PyMC to allow type checking
    class PymcModel:
        pass
else:
    from pymc import Model as PymcModel


DIRECTION_IDX = {
    "strike_slip": slice(None, None, 2),
    "dip_slip": slice(1, None, 2),
}


def _constrain_field(values, lower: float | None, upper: float | None):
    """Use a sigmoid or softplus to constrain values to a range."""
    import pymc as pm

    if lower is not None and upper is not None:
        scale = upper - lower
        return pm.math.sigmoid(values) * scale + lower  # type: ignore[attr-defined]
    if lower is not None:
        return pm.math.softplus(values) + lower  # type: ignore[attr-defined]
    if upper is not None:
        return upper - pm.math.softplus(-values)  # type: ignore[attr-defined]
    return values


def _operator_mult(operator: np.ndarray, vector):
    return operator.astype("f").copy(order="F") @ vector.astype("f")


def _get_eigen_modes(
    model: Model,
    mesh: int,
    kind: Literal["strike_slip", "dip_slip"],
    operators: Operators,
    out_idx: slice,
):
    """Get the eigenmodes and station velocity operator for a mesh and slip type."""
    assert operators.eigen is not None

    if kind == "strike_slip":
        n_eigs = model.meshes[mesh].config.n_modes_strike_slip
        start_idx = 0
    else:
        n_eigs = model.meshes[mesh].config.n_modes_dip_slip
        start_idx = model.meshes[mesh].config.n_modes_strike_slip

    eigenvectors = operators.eigen.eigenvectors_to_tde_slip[mesh][
        out_idx, start_idx : start_idx + n_eigs
    ]
    to_velocity = operators.eigen.eigen_to_velocities[mesh][
        :, start_idx : start_idx + n_eigs
    ]
    # return _clean_operator(eigenvectors), _clean_operator(to_velocity)
    return eigenvectors, to_velocity


def _station_vel_from_elastic_mesh(
    model: Model,
    mesh: int,
    kind: Literal["strike_slip", "dip_slip"],
    elastic,
    operators: Operators,
):
    """Compute elastic velocity at stations from slip rates on a mesh.

    Parameters
    ----------
    model : Model
        The model instance
    mesh : int
        Index of the mesh
    kind : Literal["strike_slip", "dip_slip"]
        Type of slip
    elastic : array
        Elastic slip rates on the mesh
    operators : Operators
        Operators containing TDE and eigen information

    Returns
    -------
    array
        Elastic velocities at station locations (flattened, all 3 components)
    """
    import pytensor.tensor as pt

    assert operators.tde is not None
    idx = DIRECTION_IDX[kind]
    method = model.config.mcmc_station_velocity_method

    if method == "low_rank":
        to_station = operators.tde.tde_to_velocities[mesh][:, idx.start : None : 3]
        u, s, vh = linalg.svd(to_station, full_matrices=False)
        threshold = 1e-5
        mask = s > threshold
        s = s[mask].astype("f")
        u = u[:, mask].astype("f")
        vh = vh[mask, :].astype("f")
        elastic_velocity = _operator_mult(-u * s, _operator_mult(vh, elastic))
        return elastic_velocity.astype("d")
    elif method == "project_to_eigen":
        assert operators.eigen is not None
        eigenvectors, to_velocity = _get_eigen_modes(
            model,
            mesh,
            kind,
            operators,
            out_idx=idx,
        )
        # TODO: This assumes that the eigenvectors are orthogonal
        # with respect to the euclidean inner product. If we change
        # the eigen decomposition to use a different inner product,
        # we will need to change this projection.
        coefs = _operator_mult(eigenvectors.T, elastic)
        elastic_velocity = _operator_mult(to_velocity, coefs)
        # We need to return a station velocity for all three components,
        # not just north and east.
        elastic_velocity = pt.concatenate(
            [
                elastic_velocity.reshape((len(model.station), 2)),
                np.zeros((len(model.station), 1)),
            ],
            axis=-1,
        ).ravel()
        return elastic_velocity
    elif method == "direct":
        to_station = operators.tde.tde_to_velocities[mesh][:, idx.start : None : 3]
        elastic_velocity = _operator_mult(-to_station, elastic)
        return elastic_velocity
    else:
        raise ValueError(
            f"Unknown mcmc_station_velocity_method: {method}. "
            "Must be one of 'direct', 'low_rank', or 'project_to_eigen'."
        )


def _mesh_component(
    model: Model,
    mesh: int,
    rotation,
    operators: Operators,
    coupling_coefs,
    elastic_eigen,
):
    import pymc as pm
    import pytensor.tensor as pt

    assert operators.eigen is not None
    assert operators.tde is not None

    mesh_obj = model.meshes[mesh]
    n_tde = mesh_obj.n_tde

    # Check constraints for each slip type
    coupling_limit_ss = mesh_obj.config.coupling_constraints_ss
    coupling_limit_ds = mesh_obj.config.coupling_constraints_ds
    rate_limit_ss = mesh_obj.config.elastic_constraints_ss
    rate_limit_ds = mesh_obj.config.elastic_constraints_ds

    has_coupling_ss = (
        coupling_limit_ss.lower is not None or coupling_limit_ss.upper is not None
    )
    has_coupling_ds = (
        coupling_limit_ds.lower is not None or coupling_limit_ds.upper is not None
    )
    has_rate_limit_ss = rate_limit_ss.lower is not None or rate_limit_ss.upper is not None
    has_rate_limit_ds = rate_limit_ds.lower is not None or rate_limit_ds.upper is not None

    # Validate constraints
    if has_rate_limit_ss and has_coupling_ss:
        raise ValueError(
            "Cannot have both rate and coupling constraints "
            f"for mesh {mesh} strike_slip."
        )
    if has_rate_limit_ds and has_coupling_ds:
        raise ValueError(
            "Cannot have both rate and coupling constraints "
            f"for mesh {mesh} dip_slip."
        )

    # Initialize containers for kinematic, coupling, and elastic
    kinematic_list = []
    coupling_list = []
    elastic_list = []
    elastic_velocity_list = []

    # Process each slip type
    for slip_type_idx, kind in enumerate(["strike_slip", "dip_slip"]):
        idx = DIRECTION_IDX[kind]

        if kind == "strike_slip":
            coupling_limit = coupling_limit_ss
            rate_limit = rate_limit_ss
            has_coupling = has_coupling_ss
            has_rate_limit = has_rate_limit_ss
        else:
            coupling_limit = coupling_limit_ds
            rate_limit = rate_limit_ds
            has_coupling = has_coupling_ds
            has_rate_limit = has_rate_limit_ds

        if has_coupling:
            # Coupling component
            if mesh not in operators.rotation_to_tri_slip_rate:
                raise ValueError(
                    f"Mesh {mesh} does not have well defined kinematic slip rates. "
                    "Coupling constraints cannot be used."
                )

            operator = operators.rotation_to_tri_slip_rate[mesh][idx, :]
            kinematic = _operator_mult(operator, rotation)
            kinematic_list.append(kinematic)

            eigenvectors, _ = _get_eigen_modes(
                model,
                mesh,
                kind,
                operators,
                out_idx=idx,
            )
            n_eigs = eigenvectors.shape[1]
            assert coupling_coefs is not None
            coefs = coupling_coefs[mesh, slip_type_idx, :n_eigs]

            coupling_field = _operator_mult(eigenvectors, coefs)
            coupling_field = _constrain_field(
                coupling_field, coupling_limit.lower, coupling_limit.upper
            )
            coupling_list.append(coupling_field)

            elastic = kinematic * coupling_field
            elastic_list.append(elastic)

            elastic_velocity = _station_vel_from_elastic_mesh(
                model,
                mesh,
                kind,
                elastic,
                operators,
            )
            elastic_velocity_list.append(elastic_velocity)

        elif has_rate_limit:
            # Elastic component
            eigenvectors, to_velocity = _get_eigen_modes(
                model,
                mesh,
                kind,
                operators,
                out_idx=idx,
            )
            n_eigs = eigenvectors.shape[1]
            assert elastic_eigen is not None
            param = elastic_eigen[mesh, slip_type_idx, :n_eigs]

            elastic = _constrain_field(
                _operator_mult(eigenvectors, param), rate_limit.lower, rate_limit.upper
            )
            elastic_list.append(elastic)

            if rate_limit.lower is None and rate_limit.upper is None:
                elastic_velocity = _operator_mult(to_velocity, param)
                elastic_velocity = pt.concatenate(
                    [
                        elastic_velocity.reshape((len(model.station), 2)),
                        np.zeros((len(model.station), 1)),
                    ],
                    axis=-1,
                ).ravel()
            else:
                elastic_velocity = _station_vel_from_elastic_mesh(
                    model,
                    mesh,
                    kind,
                    elastic,
                    operators,
                )
            elastic_velocity_list.append(elastic_velocity)

    # Return values to be collected and stacked in _build_pymc_model
    # Ensure all arrays have shape (2, n_tde) by padding with zeros for unused slip types
    kinematic_stacked = None
    coupling_stacked = None
    elastic_stacked = None
    
    if kinematic_list:
        # Ensure we have exactly 2 elements (one for each slip type)
        # If only one slip type is used, pad with zeros
        if len(kinematic_list) == 1:
            # Add a zero array for the missing slip type
            # Determine which slip type is missing based on which constraints are set
            if has_coupling_ss and not has_coupling_ds:
                # Only strike_slip, add zeros for dip_slip
                zero_kinematic = pt.zeros_like(kinematic_list[0])
                kinematic_list.append(zero_kinematic)
            elif has_coupling_ds and not has_coupling_ss:
                # Only dip_slip, add zeros for strike_slip
                zero_kinematic = pt.zeros_like(kinematic_list[0])
                kinematic_list.insert(0, zero_kinematic)
        # Stack kinematic rates: shape will be (2, n_tde) for strike_slip and dip_slip
        kinematic_stacked = pt.stack(kinematic_list, axis=0)

    if coupling_list:
        # Ensure we have exactly 2 elements
        if len(coupling_list) == 1:
            if has_coupling_ss and not has_coupling_ds:
                zero_coupling = pt.zeros_like(coupling_list[0])
                coupling_list.append(zero_coupling)
            elif has_coupling_ds and not has_coupling_ss:
                zero_coupling = pt.zeros_like(coupling_list[0])
                coupling_list.insert(0, zero_coupling)
        coupling_stacked = pt.stack(coupling_list, axis=0)

    if elastic_list:
        # Ensure we have exactly 2 elements
        if len(elastic_list) == 1:
            # Determine which slip type is missing
            if (has_coupling_ss or has_rate_limit_ss) and not (has_coupling_ds or has_rate_limit_ds):
                # Only strike_slip, add zeros for dip_slip
                zero_elastic = pt.zeros_like(elastic_list[0])
                elastic_list.append(zero_elastic)
            elif (has_coupling_ds or has_rate_limit_ds) and not (has_coupling_ss or has_rate_limit_ss):
                # Only dip_slip, add zeros for strike_slip
                zero_elastic = pt.zeros_like(elastic_list[0])
                elastic_list.insert(0, zero_elastic)
        elastic_stacked = pt.stack(elastic_list, axis=0)

    # Sum elastic velocities for station likelihood
    # This should always have at least one element since we process both slip types
    elastic_velocity = sum(elastic_velocity_list)
    
    return {
        "kinematic": kinematic_stacked,
        "coupling": coupling_stacked,
        "elastic": elastic_stacked,
        "elastic_velocity": elastic_velocity,
    }


def _add_block_strain_rate_component(operators: Operators):
    """Add block strain rate component to the PyMC model.

    Returns the velocity contribution from block strain rates.
    """
    import pymc as pm

    raw = pm.Normal("block_strain_rate_raw", sigma=100, dims="block_strain_rate_param")
    if operators.block_strain_rate_to_velocities.size == 0:
        scale = 1.0
    else:
        scale = 1 / np.sqrt((operators.block_strain_rate_to_velocities**2).mean())
    block_strain_rate = pm.Deterministic(
        "block_strain_rate", scale * raw, dims="block_strain_rate_param"
    )

    return _operator_mult(operators.block_strain_rate_to_velocities, block_strain_rate)


def _add_rotation_component(operators: Operators):
    """Add block rotation component to the PyMC model.

    Returns rotation parameters and velocity contributions.
    """
    import pymc as pm

    A = (
        operators.rotation_to_velocities
        - operators.rotation_to_slip_rate_to_okada_to_velocities
    )
    scale = 1e6
    B = A / scale
    u, s, vh = linalg.svd(B, full_matrices=False)
    raw = pm.StudentT("rotation_raw", sigma=20, nu=4, dims="rotation_param")

    rotation = pm.Deterministic(
        "rotation", _operator_mult(vh.T, raw / scale), dims="rotation_param"
    )

    rotation_velocity = _operator_mult(operators.rotation_to_velocities, rotation)
    rotation_okada_velocity = _operator_mult(
        -operators.rotation_to_slip_rate_to_okada_to_velocities, rotation
    )

    return rotation, rotation_velocity, rotation_okada_velocity


def _add_mogi_component(operators: Operators):
    """Add Mogi source component to the PyMC model.

    Returns the velocity contribution from Mogi sources.
    """
    import pymc as pm

    raw = pm.Normal("mogi_raw", dims="mogi_param")
    if operators.mogi_to_velocities.size == 0:
        scale = 1.0
    else:
        scale = 1 / np.sqrt((operators.mogi_to_velocities**2).mean())
    mogi = pm.Deterministic("mogi", scale * raw, dims="mogi_param")

    return _operator_mult(operators.mogi_to_velocities, mogi)


def _add_station_velocity_likelihood(model: Model, mu):
    """Add station velocity likelihood to the PyMC model.

    Uses area-weighted Student-t likelihood for station observations.
    """
    import pymc as pm

    sigma = pm.HalfNormal("sigma", sigma=2)
    data = np.array([model.station.east_vel, model.station.north_vel]).T

    lh_dist = pm.StudentT.dist

    def lh(value, weight, mu, sigma):
        dist = lh_dist(nu=6, mu=mu, sigma=sigma)
        return weight * pm.logp(dist, value)

    def random(weight, mu, sigma, rng=None, size=None):
        return lh_dist(nu=6, mu=mu, sigma=sigma, rng=rng, size=size)

    if model.config.mcmc_station_weighting is None:
        logger.info(f"Using unweighted station likelihood ({len(data)} stations)")
        pm.StudentT(
            "station_velocity",
            mu=mu,
            sigma=sigma,
            observed=data,
            dims=("station", "xy"),
            nu=6,
        )
    elif model.config.mcmc_station_weighting == "voronoi":
        effective_area = model.config.mcmc_station_effective_area

        voroni = spatial.SphericalVoronoi(
            model.station[["x", "y", "z"]].values, RADIUS_EARTH
        )
        areas = voroni.calculate_areas()

        areas_clipped = np.minimum(effective_area, areas)
        weight = areas_clipped / effective_area

        # Log diagnostics about the weighting
        effective_n = (weight.sum() ** 2) / (weight**2).sum()
        logger.info("Station weighting diagnostics:")
        logger.info(f"  Number of stations: {len(weight)}")
        logger.info(
            f"  Effective area threshold: {np.sqrt(effective_area) / 1000:.1f} km "
            f"x {np.sqrt(effective_area) / 1000:.1f} km"
        )
        logger.info(f"  Weight range: [{weight.min():.3f}, {weight.max():.3f}]")
        logger.info(
            f"  Effective sample size: {effective_n:.1f} (vs {len(weight)} stations)"
        )
        logger.info(
            "  Stations at full weight (area >= threshold): "
            f"{(areas >= effective_area).sum()}"
        )

        pm.CustomDist(
            "station_velocity",
            weight[:, None],
            mu,
            sigma,
            logp=lh,
            random=random,
            observed=data,
            dims=("station", "xy"),
        )
    else:
        raise ValueError(
            f"Unknown mcmc_station_weighting: {model.config.mcmc_station_weighting}. "
            "Must be None or 'voronoi'."
        )


def _add_segment_constraints(model: Model, operators: Operators, rotation):
    """Add segment slip rate constraints to the PyMC model.

    Includes regularization, observations, and bounds on slip rates.
    """
    import pymc as pm

    segment_rates = _operator_mult(operators.rotation_to_slip_rate, rotation)
    segment_rates = segment_rates.reshape((-1, 3))

    # Define slip type coordinates (must match coords in _build_pymc_model)
    slip_type_coords = ["strike_slip", "dip_slip", "tensile_slip"]
    abbrev_map = {
        "strike_slip": "ss",
        "dip_slip": "ds",
        "tensile_slip": "ts",
    }

    # Regularization towards zero slip rate
    gamma = model.config.segment_slip_rate_regularization_sigma
    if gamma is not None:
        for i, slip_type in enumerate(slip_type_coords):
            abbrev = abbrev_map[slip_type]
            pm.StudentT(
                f"segment_slip_rate_regularization_{abbrev}",
                mu=segment_rates[
                    (model.segment[f"{abbrev}_rate_flag"] == 2).values, i
                ],
                sigma=gamma,
                nu=5,
                observed=np.zeros((model.segment[f"{abbrev}_rate_flag"] == 2).sum()),
            )

    pm.Deterministic("segment_slip_rate", segment_rates, dims=("segment", "slip_type"))

    # Slip rate observations
    for comp, flag_attr, rate_attr, sig_attr in [
        ("strike_slip", "ss_rate_flag", "ss_rate", "ss_rate_sig"),
        ("dip_slip", "ds_rate_flag", "ds_rate", "ds_rate_sig"),
        ("tensile_slip", "ts_rate_flag", "ts_rate", "ts_rate_sig"),
    ]:
        flags = getattr(model.segment, flag_attr).values
        if np.any(flags):
            observed_rates = getattr(model.segment, rate_attr).values[flags == 1]
            observed_sigs = getattr(model.segment, sig_attr).values[flags == 1]
            comp_idx = slip_type_coords.index(comp)
            pm.Normal(
                f"segment_{comp}_velocity",
                mu=segment_rates[flags == 1, comp_idx],
                sigma=observed_sigs,
                observed=observed_rates,
            )

    # Slip rate bounds (soft constraints)
    for comp, bound_flag_attr, lower_attr, upper_attr in [
        (
            "strike_slip",
            "ss_rate_bound_flag",
            "ss_rate_bound_min",
            "ss_rate_bound_max",
        ),
        (
            "dip_slip",
            "ds_rate_bound_flag",
            "ds_rate_bound_min",
            "ds_rate_bound_max",
        ),
        (
            "tensile_slip",
            "ts_rate_bound_flag",
            "ts_rate_bound_min",
            "ts_rate_bound_max",
        ),
    ]:
        bound_flags = getattr(model.segment, bound_flag_attr).values
        if np.any(bound_flags):
            lower_bounds = getattr(model.segment, lower_attr).values[bound_flags == 1]
            upper_bounds = getattr(model.segment, upper_attr).values[bound_flags == 1]
            bound_sig = model.config.segment_slip_rate_bound_sigma
            comp_idx = slip_type_coords.index(comp)
            pm.Censored(
                f"segment_{comp}_slip_rate_lower_bound",
                dist=pm.Normal.dist(
                    mu=segment_rates[bound_flags == 1, comp_idx],
                    sigma=bound_sig,
                ),
                upper=lower_bounds,
                lower=None,
                observed=lower_bounds,
            )

            pm.Censored(
                f"segment_{comp}_slip_rate_upper_bound",
                dist=pm.Normal.dist(
                    mu=segment_rates[bound_flags == 1, comp_idx],
                    sigma=bound_sig,
                ),
                upper=None,
                lower=upper_bounds,
                observed=upper_bounds,
            )


def _build_pymc_model(model: Model, operators: Operators) -> PymcModel:
    """Build the complete PyMC model for MCMC inference.

    Combines all velocity components (block strain, rotation, Mogi, elastic)
    and adds likelihoods for station and segment observations.
    """
    assert operators.eigen is not None
    assert operators.tde is not None

    import pymc as pm
    import pytensor.tensor as pt

    # Calculate maximum number of eigenmodes across all meshes and slip types
    max_n_eigenmodes = 0
    max_n_tde = 0
    for mesh in model.meshes:
        max_n_eigenmodes = max(
            max_n_eigenmodes,
            mesh.config.n_modes_strike_slip,
            mesh.config.n_modes_dip_slip,
        )
        max_n_tde = max(max_n_tde, mesh.n_tde)

    coords = {
        "block_strain_rate_param": pd.RangeIndex(
            operators.block_strain_rate_to_velocities.shape[1]
        ),
        "global_float_block_rotation_param": pd.RangeIndex(
            operators.global_float_block_rotation.shape[1]
        ),
        "mogi_param": pd.RangeIndex(operators.mogi_to_velocities.shape[1]),
        "rotation_param": pd.RangeIndex(operators.rotation_to_velocities.shape[1]),
        "station": model.station.index,
        "segment": model.segment.index,
        "xyz": pd.Index(["x", "y", "z"]),
        "xy": pd.Index(["x", "y"]),
        "slip_type": pd.Index(["strike_slip", "dip_slip", "tensile_slip"]),
        "eigenmode": pd.RangeIndex(max_n_eigenmodes),
        "mesh": pd.RangeIndex(len(model.meshes)),
        "tde": pd.RangeIndex(max_n_tde),
    }

    with pm.Model(coords=coords) as pymc_model:
        # Add velocity components
        block_strain_rate_velocity = _add_block_strain_rate_component(operators)
        rotation, rotation_velocity, rotation_okada_velocity = _add_rotation_component(
            operators
        )
        mogi_velocity = _add_mogi_component(operators)

        # Check which meshes need coupling vs elastic variables
        needs_coupling = []
        needs_elastic = []
        for mesh_idx, mesh in enumerate(model.meshes):
            has_coupling_ss = (
                mesh.config.coupling_constraints_ss.lower is not None
                or mesh.config.coupling_constraints_ss.upper is not None
            )
            has_coupling_ds = (
                mesh.config.coupling_constraints_ds.lower is not None
                or mesh.config.coupling_constraints_ds.upper is not None
            )
            has_rate_limit_ss = (
                mesh.config.elastic_constraints_ss.lower is not None
                or mesh.config.elastic_constraints_ss.upper is not None
            )
            has_rate_limit_ds = (
                mesh.config.elastic_constraints_ds.lower is not None
                or mesh.config.elastic_constraints_ds.upper is not None
            )
            if has_coupling_ss or has_coupling_ds:
                needs_coupling.append(mesh_idx)
            if has_rate_limit_ss or has_rate_limit_ds:
                needs_elastic.append(mesh_idx)

        # Create shared variables with mesh dimension
        coupling_coefs = None
        if needs_coupling:
            coupling_coefs = pm.Normal(
                "coupling_coefs",
                mu=0,
                sigma=10,
                dims=("mesh", "slip_type", "eigenmode"),
            )

        elastic_eigen_raw = None
        elastic_eigen = None
        if needs_elastic:
            # Calculate scale
            scale = 0.0
            for op in operators.eigen.eigen_to_velocities.values():
                scale += (op**2).mean()
            scale = scale / len(operators.eigen.eigen_to_velocities)
            scale = 1 / np.sqrt(scale)

            elastic_eigen_raw = pm.Normal(
                "elastic_eigen_raw",
                dims=("mesh", "slip_type", "eigenmode"),
            )
            elastic_eigen = pm.Deterministic(
                "elastic_eigen",
                scale * elastic_eigen_raw,
                dims=("mesh", "slip_type", "eigenmode"),
            )

        # Collect kinematic, coupling, and elastic from all meshes
        all_kinematic = []
        all_coupling = []
        all_elastic = []
        elastic_velocities = []
        
        for key, _ in enumerate(model.meshes):
            result = _mesh_component(
                model,
                key,
                rotation,
                operators,
                coupling_coefs,
                elastic_eigen,
            )
            elastic_velocities.append(result["elastic_velocity"])
            if result["kinematic"] is not None:
                all_kinematic.append((key, result["kinematic"]))
            if result["coupling"] is not None:
                all_coupling.append((key, result["coupling"]))
            if result["elastic"] is not None:
                all_elastic.append((key, result["elastic"]))
        
        # Create shared Deterministic variables with mesh dimension
        # Note: We need to handle variable n_tde per mesh
        # Pad to max_n_tde when needed to ensure all arrays have shape (2, max_n_tde)
        if all_kinematic:
            # Stack all kinematic values, padding to max_n_tde
            kinematic_padded = []
            for mesh_idx, kinematic in all_kinematic:
                n_tde = model.meshes[mesh_idx].n_tde
                # Always ensure shape is exactly (2, max_n_tde)
                if n_tde < max_n_tde:
                    padding = pt.zeros((2, max_n_tde - n_tde))
                    padded = pt.concatenate([kinematic, padding], axis=1)
                elif n_tde == max_n_tde:
                    padded = kinematic
                else:
                    # Shouldn't happen, but handle it
                    padded = kinematic
                kinematic_padded.append(padded)
            kinematic_stacked = pt.stack(kinematic_padded, axis=0)
            pm.Deterministic("kinematic", kinematic_stacked, dims=("mesh", "slip_type", "tde"))
        
        if all_coupling:
            coupling_padded = []
            for mesh_idx, coupling in all_coupling:
                n_tde = model.meshes[mesh_idx].n_tde
                if n_tde < max_n_tde:
                    padding = pt.zeros((2, max_n_tde - n_tde))
                    padded = pt.concatenate([coupling, padding], axis=1)
                    coupling_padded.append(padded)
                else:
                    coupling_padded.append(coupling)
            coupling_stacked = pt.stack(coupling_padded, axis=0)
            pm.Deterministic("coupling", coupling_stacked, dims=("mesh", "slip_type", "tde"))
        
        if all_elastic:
            elastic_padded = []
            for mesh_idx, elastic in all_elastic:
                n_tde = model.meshes[mesh_idx].n_tde
                if n_tde < max_n_tde:
                    padding = pt.zeros((2, max_n_tde - n_tde))
                    padded = pt.concatenate([elastic, padding], axis=1)
                    elastic_padded.append(padded)
                else:
                    elastic_padded.append(elastic)
            elastic_stacked = pt.stack(elastic_padded, axis=0)
            pm.Deterministic("elastic", elastic_stacked, dims=("mesh", "slip_type", "tde"))
        
        elastic_velocity = sum(elastic_velocities)

        # Combine all velocity components
        mu = (
            block_strain_rate_velocity
            + rotation_velocity
            + rotation_okada_velocity
            + mogi_velocity
            + elastic_velocity
        )
        mu = mu.reshape((len(model.station), 3))[:, :2]
        pm.Deterministic("mu", mu, dims=("station", "xy"))

        # Add likelihoods and constraints
        _add_station_velocity_likelihood(model, mu)
        _add_segment_constraints(model, operators, rotation)

    return pymc_model


def solve_mcmc(
    model: Model,
    *,
    operators: Operators | None = None,
    sample_kwargs: dict | None = None,
) -> Estimation:
    if importlib.util.find_spec("nutpie") is None:
        raise ImportError(
            "nutpie is required for MCMC solving. "
            "Please install it with 'pip install nutpie'."
        )
    if importlib.util.find_spec("pymc") is None:
        raise ImportError(
            "pymc is required for MCMC solving. "
            "Please install it with 'pip install pymc'."
        )

    import nutpie

    if model.config.segment_slip_rate_hard_bounds:
        raise ValueError(
            "Hard bounds on segment slip rates are not supported in MCMC solve. "
            "Please use soft bounds with `segment_slip_rate_bound_sigma` instead."
        )

    if operators is None:
        operators = build_operators(model, tde=True, eigen=True)

    if operators.tde is None or operators.eigen is None:
        raise ValueError(
            "Operators must have both TDE and eigen components for MCMC solve."
        )

    pymc_model = _build_pymc_model(model, operators)

    compiled = nutpie.compile_pymc_model(
        pymc_model,
        backend=model.config.mcmc_backend,
    )
    kwargs = {
        "low_rank_modified_mass_matrix": True,
        "mass_matrix_eigval_cutoff": 1.5,
        "mass_matrix_gamma": 1e-6,
        "chains": model.config.mcmc_chains,
        "draws": model.config.mcmc_draws,
        "tune": model.config.mcmc_tune,
        "store_unconstrained": True,
        "store_gradient": True,
        "seed": model.config.mcmc_seed,
    }
    kwargs.update(sample_kwargs or {})
    trace = nutpie.sample(compiled, **kwargs)

    operators_tde = build_operators(model, tde=True, eigen=False)
    state_vector = _state_vector_from_draw(
        model, operators_tde, trace.mean(["chain", "draw"])
    )
    estimation = build_estimation(model, operators_tde, state_vector)
    estimation.mcmc_trace = trace
    return estimation


def _state_vector_from_draw(
    model: Model,
    operators_tde: Operators,
    trace,
):
    assert operators_tde.tde is not None
    assert operators_tde.index.tde is not None
    n_params = operators_tde.full_dense_operator.shape[1]
    state_vector = np.zeros(n_params)

    start = operators_tde.index.start_block_strain_col
    end = operators_tde.index.end_block_strain_col
    state_vector[start:end] = trace.posterior.block_strain_rate.values

    start = operators_tde.index.start_mogi_col
    end = operators_tde.index.end_mogi_col
    state_vector[start:end] = trace.posterior.mogi.values

    start = operators_tde.index.start_block_col
    end = operators_tde.index.end_block_col
    state_vector[start:end] = trace.posterior.rotation.values

    for mesh_idx in range(len(model.meshes)):
        indices = {
            "strike_slip": slice(None, None, 2),
            "dip_slip": slice(1, None, 2),
        }
        for name, idx in indices.items():
            start = operators_tde.index.tde.start_tde_col[mesh_idx]
            end = operators_tde.index.tde.end_tde_col[mesh_idx]
            var_name = f"elastic_{mesh_idx}_{name}"

            if var_name in trace.posterior:
                vals = trace.posterior[var_name]
                # if there is only one of strike/dip slip
                if vals.shape == state_vector[start:end].shape:
                    state_vector[start:end] = vals
                else:
                    state_vector[start:end][idx] = trace.posterior[var_name].values
    return state_vector
