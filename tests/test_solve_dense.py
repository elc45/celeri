import pytest
import celeri
import numpy as np

@pytest.mark.array_compare(atol=1e-10)
@pytest.mark.parametrize(
    "config_name",
    ["test_japan_config", "test_wna_config"],
)
def test_operator_tde_to_velocities(config_name):
    config_file = f"./tests/configs/{config_name}.json"
    config = celeri.get_config(config_file)
    model = celeri.build_model(config)

    estimation = celeri.assemble_and_solve_dense(model, eigen=True, tde=True)

    assert estimation.operators.tde is not None

    operator = estimation.operators.tde.tde_to_velocities[0]
    rng = np.random.default_rng(seed=0)
    size = min(min(len(operator), len(operator[0])), 50)
    idx_rows = rng.choice(len(operator), size=size, replace=False)
    idx_cols = rng.choice(len(operator[0]), size=size, replace=False)

    return operator[np.ix_(idx_rows, idx_cols)]


@pytest.mark.array_compare(atol=1e-10)
@pytest.mark.parametrize(
    "config_name",
    ["test_japan_config", "test_wna_config"],
)
def test_operator_eigen_to_velocities(config_name):
    config_file = f"./tests/configs/{config_name}.json"
    config = celeri.get_config(config_file)
    model = celeri.build_model(config)

    estimation = celeri.assemble_and_solve_dense(model, eigen=True, tde=True)

    assert estimation.operators.eigen is not None

    operator = estimation.operators.eigen.eigen_to_velocities[0]
    rng = np.random.default_rng(seed=0)
    size = min(min(len(operator), len(operator[0])), 50)
    idx_rows = rng.choice(len(operator), size=size, replace=False)
    idx_cols = rng.choice(len(operator[0]), size=size, replace=False)

    return operator[np.ix_(idx_rows, idx_cols)]


@pytest.mark.array_compare(atol=1e-10)
@pytest.mark.parametrize(
    "config_name",
    ["test_japan_config", "test_wna_config"],
)
def test_operator_eigen_to_tde_slip(config_name):
    config_file = f"./tests/configs/{config_name}.json"
    config = celeri.get_config(config_file)
    model = celeri.build_model(config)

    estimation = celeri.assemble_and_solve_dense(model, eigen=True, tde=True)

    assert estimation.operators.eigen is not None

    operator = estimation.operators.eigen.eigenvectors_to_tde_slip[0]
    rng = np.random.default_rng(seed=0)
    size = min(min(len(operator), len(operator[0])), 50)
    idx_rows = rng.choice(len(operator), size=size, replace=False)
    idx_cols = rng.choice(len(operator[0]), size=size, replace=False)

    return operator[np.ix_(idx_rows, idx_cols)]


@pytest.mark.array_compare(atol=1e-10)
@pytest.mark.parametrize(
    "config_name",
    ["test_japan_config", "test_wna_config"],
)
def test_operator_eigen_to_tde_bcs(config_name):
    config_file = f"./tests/configs/{config_name}.json"
    config = celeri.get_config(config_file)
    model = celeri.build_model(config)

    estimation = celeri.assemble_and_solve_dense(model, eigen=True, tde=True)

    assert estimation.operators.eigen is not None

    operator = estimation.operators.eigen.eigen_to_tde_bcs[0]
    rng = np.random.default_rng(seed=0)
    size = min(min(len(operator), len(operator[0])), 50)
    idx_rows = rng.choice(len(operator), size=size, replace=False)
    idx_cols = rng.choice(len(operator[0]), size=size, replace=False)

    return operator[np.ix_(idx_rows, idx_cols)]


@pytest.mark.array_compare(atol=1e-10)
@pytest.mark.parametrize(
    "config_name",
    ["test_japan_config", "test_wna_config"],
)
def test_operator_slip_rate_to_okada_to_velocities(config_name):
    config_file = f"./tests/configs/{config_name}.json"
    config = celeri.get_config(config_file)
    model = celeri.build_model(config)

    estimation = celeri.assemble_and_solve_dense(model, eigen=True, tde=True)

    assert estimation.operators.slip_rate_to_okada_to_velocities is not None

    operator = estimation.operators.slip_rate_to_okada_to_velocities
    rng = np.random.default_rng(seed=0)
    size = min(min(len(operator), len(operator[0])), 50)
    idx_rows = rng.choice(len(operator), size=size, replace=False)
    idx_cols = rng.choice(len(operator[0]), size=size, replace=False)

    return operator[np.ix_(idx_rows, idx_cols)]


@pytest.mark.array_compare(atol=1e-10)
@pytest.mark.parametrize(
    "config_name",
    ["test_japan_config", "test_wna_config"],
)
def test_operator_block_strain_rate_to_velocities(config_name):
    config_file = f"./tests/configs/{config_name}.json"
    config = celeri.get_config(config_file)
    model = celeri.build_model(config)

    estimation = celeri.assemble_and_solve_dense(model, eigen=True, tde=True)

    assert estimation.operators.block_strain_rate_to_velocities is not None

    operator = estimation.operators.block_strain_rate_to_velocities
    rng = np.random.default_rng(seed=0)
    size = min(min(len(operator), len(operator[0])), 50)
    idx_rows = rng.choice(len(operator), size=size, replace=False)
    idx_cols = rng.choice(len(operator[0]), size=size, replace=False)

    return operator[np.ix_(idx_rows, idx_cols)]

@pytest.mark.array_compare(atol=1e-10)
@pytest.mark.parametrize(
    "config_name",
    ["test_japan_config", "test_wna_config"],
)
def test_operator_rotation_to_slip_rate(config_name):
    config_file = f"./tests/configs/{config_name}.json"
    config = celeri.get_config(config_file)
    model = celeri.build_model(config)

    estimation = celeri.assemble_and_solve_dense(model, eigen=True, tde=True)

    assert estimation.operators.rotation_to_slip_rate is not None

    operator = estimation.operators.rotation_to_slip_rate
    rng = np.random.default_rng(seed=0)
    size = min(min(len(operator), len(operator[0])), 50)
    idx_rows = rng.choice(len(operator), size=size, replace=False)
    idx_cols = rng.choice(len(operator[0]), size=size, replace=False)

    return operator[np.ix_(idx_rows, idx_cols)]


@pytest.mark.array_compare(atol=1e-10)
@pytest.mark.parametrize(
    "config_name",
    ["test_japan_config", "test_wna_config"],
)
def test_operator_rotation_to_tri_slip_rate(config_name):
    config_file = f"./tests/configs/{config_name}.json"
    config = celeri.get_config(config_file)
    model = celeri.build_model(config)

    estimation = celeri.assemble_and_solve_dense(model, eigen=True, tde=True)

    assert estimation.operators.rotation_to_tri_slip_rate is not None

    operator = estimation.operators.rotation_to_tri_slip_rate[0]
    rng = np.random.default_rng(seed=0)
    size = min(min(len(operator), len(operator[0])), 50)
    idx_rows = rng.choice(len(operator), size=size, replace=False)
    idx_cols = rng.choice(len(operator[0]), size=size, replace=False)

    return operator[np.ix_(idx_rows, idx_cols)]


@pytest.mark.array_compare(atol=1e-10)
@pytest.mark.parametrize(
    "config_name, eigen, tde",
    [
        ("test_japan_config", True, True),
        ("test_japan_config", False, True),
        ("test_japan_config", False, False),
        ("test_wna_config", True, True),
        ("test_wna_config", False, True),
        ("test_wna_config", False, False),
    ],
)
def test_dense_sol(config_name, eigen: bool, tde: bool):
    config_file = f"./tests/configs/{config_name}.json"
    config = celeri.get_config(config_file)
    model = celeri.build_model(config)

    estimation = celeri.assemble_and_solve_dense(model, eigen=eigen, tde=tde)

    scale_factors = {
    'block_rotation': 1e6,
    'block_strain': 1e7,
    'mogi': 1e-9,               
    'eigen': 1e-3,              
    }

    index = estimation.index
    n_params = len(estimation.state_vector)
    scaling_vector = np.ones(n_params)

    if index.start_block_col < index.end_block_col:
        scaling_vector[index.start_block_col:index.end_block_col] = scale_factors['block_rotation']

    if index.start_block_strain_col < index.end_block_strain_col:
        scaling_vector[index.start_block_strain_col:index.end_block_strain_col] = scale_factors['block_strain']

    if index.start_mogi_col < index.end_mogi_col:
        scaling_vector[index.start_mogi_col:index.end_mogi_col] = scale_factors['mogi']

    if eigen:
        assert index.eigen is not None
        for mesh_idx in range(index.n_meshes):
            start = index.eigen.start_col_eigen[mesh_idx]
            end = index.eigen.end_col_eigen[mesh_idx]
            if start < end and end <= n_params:
                scaling_vector[start:end] = scale_factors['eigen']

    state_vector_scaled = estimation.state_vector * scaling_vector
    return state_vector_scaled


def test_japan_dense_error():
    config_file_name = "./tests/configs/test_japan_config.json"
    model = celeri.build_model(config_file_name)

    with pytest.raises(ValueError):
        celeri.assemble_and_solve_dense(model, eigen=True, tde=False)
    return
