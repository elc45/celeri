All of these have been removed/updated in the `*mesh.json` files in the celeri repository.


`"smoothing_weight"`: float, weight for Laplacian smoothing

`"n_modes_strike_slip"`: int, number of eigenmodes in the strike-slip direction

`"n_modes_dip_slip"`: int, number of eigenmodes in the dip-slip direction

`"top_slip_rate_constraint"`: int, 0/1 flag to force slip on top elements to zero

`"bot_slip_rate_constraint"`: int, 0/1 flag to force slip on bottom elements to zero

`"side_slip_rate_constraint"`: int, 0/1 flag to force slip on side elements to zero

`"top_slip_rate_weight"`: float, weight for zero-slip constraint on top elements

`"bot_slip_rate_weight"`: float, weight for zero-slip constraint on bottom elements

`"side_slip_rate_weight"`: float, weight for zero-slip constraint on side elements

`"a_priori_slip_filename"`: string, filename containing a priori slip rates (not currently used but we may so keeping)

`"ss_slip_constraint_idx"`: array, element indices for a priori strike-slip rates

`"ss_slip_constraint_rate"`: array, a priori strike-slip rates

`"ds_slip_constraint_idx"`: array, element indices for a priori dip-slip rates

`"ds_slip_constraint_rate"`: array, a priori dip-slip rates

`"qp_mesh_tde_slip_rate_lower_bound_ss"`: float, QP strike-slip rate lower bound

`"qp_mesh_tde_slip_rate_upper_bound_ss"`: float, QP strike-slip rate upper bound

`"qp_mesh_tde_slip_rate_lower_bound_ds"`: float, QP dip-slip rate lower bound

`"qp_mesh_tde_slip_rate_upper_bound_ds"`: float, QP dip-slip rate upper bound

`"qp_mesh_tde_slip_rate_lower_bound_ss_coupling"`: float, QP strike-slip coupling lower bound

`"qp_mesh_tde_slip_rate_upper_bound_ss_coupling"`: float, QP strike-slip coupling upper bound

`"qp_mesh_tde_slip_rate_lower_bound_ds_coupling"`: float, QP dip-slip coupling lower bound

`"qp_mesh_tde_slip_rate_upper_bound_ds_coupling"`: float, QP dip-slip coupling upper bound

`"iterative_coupling_smoothing_length_scale"`: float, length scale for smoothing kinematic slip distribution for bounded coupling. Squared in the denominator of the Gaussian smoothing operator

`"iterative_coupling_linear_slip_rate_reduction_factor"`: float (<1), adjustment factor for each iteration's reduction of slip rate bounds

`"iterative_coupling_kinematic_slip_regularization_scale"`: float (>0), absolute value of minimum kinematic slip rate (to prevent coupling from blowing up at kinematic rates of zero.  @brendanjmeade Unused?)

`"mesh_tde_modes_bc_weight"`: float, weight of slip rate constraints for eigenmode approach