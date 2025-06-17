`"apriori_block_name"`: string, name of file containing a priori constraints on block rotation. *Flagged as unexpected after refactor*

`"atol"`: float, Primary tolerance for H-matrix solve

`"base_runs_folder"`: string, path to folder holding celeri runs

`"block_constraint_weight"`: float, weight for a priori block rotation constraints

`"block_constraint_weight_max"`: float, max. weight for a priori block rotation constraints (unused)

`"block_constraint_weight_min"`: float, min. weight for a priori block rotation constraints (unused)

`"block_constraint_weight_steps"`: int, number of iteration steps for block constraint weights (unused)

`"block_file_name"`: string, Name of *_block.csv file

`"btol"`: float, Secondary tolerance for H-matrix solve

`"coupling_bounds_max_iter"`: int, Maximum number of coupling bound iterations

`"coupling_bounds_total_percentage_satisfied_target"`: float, Percentage of triangles that must satisfy coupling constraints

`"fault_resolution"`: float, purpose unclear (unused). *Flagged as unexpected after refactor*

`"file_name"`: string, Name of this command file (unused, because it's a required input?)

`"global_elastic_cutoff_distance"`: float, Fault-station distance beyond which elastic deformation is not calculated

`"global_elastic_cutoff_distance_flag"`: int (0/1), Flag for using elastic cutoff distance

`"h_matrix_min_pts_per_box"`: int, H-matrix minimum points per compression box

`"h_matrix_min_separation"`: float, H-matrix minimum interaction distance scaling factor

`"h_matrix_tol"`: float, H-matrix tolerance 

`"inversion_param01"`: int, unused. *Flagged as unexpected after refactor*

`"inversion_param02"`: int, unused. *Flagged as unexpected after refactor*

`"inversion_param03"`: int, unused. *Flagged as unexpected after refactor*

`"inversion_param04"`: int, unused. *Flagged as unexpected after refactor*

`"inversion_param05"`: int, unused. *Flagged as unexpected after refactor*

`"inversion_type"`: string, unused. *Flagged as unexpected after refactor*

`"iterative_solver"`: string, Interative solver type (lsqr | lsmr)

`"lat_range"`: list of floats, Range of latitudes used in plotting

`"locking_depth_flag2"`: float, test locking depth (unused)

`"locking_depth_flag3"`: float, test locking depth (unused)

`"locking_depth_flag4"`: float, test locking depth (unused)

`"locking_depth_flag5"`: float, test locking depth (unused)

`"locking_depth_overide_value"`: float, override locking depth (unused)

`"locking_depth_override_flag"`: int (0/1), flag to implement override locking depth (unused)

`"lon_range"`: list of floats, Range of longitudes used in plotting

`"material_lambda"`: float, first Lamé parameter

`"material_mu"`: float, second Lamé parameter 

`"mesh_parameters_file_name"`: string, Name of *_mesh_parameters.json file

`"mogi_file_name"`: string, Name of Mogi source *.json file

`"n_iterations"`: int, Number of general iterations (unused)

`"operators_folder"`: string, Name of folder to store elastic partials

`"output_path"`: string, Name of folder for model output

`"pickle_save"`: int, Flag for saving major data structures in pickle file (0 | 1)

`"plot_estimation_summary"`: int, Flag for saving summary plot of model results (0 | 1)

`"plot_input_summary"`: int, Flag for saving summary plot of input data (0 | 1)

`"pmag_tri_smooth"`: int, Flag for weighting Laplacian smoothing by resolution (0 | 1) (unused). *Flagged as unexpected after refactor*

`"printslipcons"`: int, Flag for printing slip constraints (0 | 1) (unused)

`"quiver_scale"`: float, Scale factor for velocity vectors in plots 

`"repl"`: int, Flag for dropping into REPL (0 | 1)

`"reuse_elastic"`: int, Flag for reusing elastic calculations (0 | 1)

`"reuse_elastic_file"`: string, Name of stored elastic calculation file

`"ridge_param"`: int, Parameter for ridge regression (unused)

`"run_name"`: string, Name of folder for storing model results (determined within celeri)

`"sar_file_name"`: string, Name of SAR LOS file name (check replacement by `"los_file_name")

`"sar_ramp"`: int, Polynomial order for SAR ramp estimation (unused). *Flagged as unexpected after refactor*

`"sar_weight"`: float, Weighting of SAR dataset. *Flagged as unexpected after refactor* 

`"save_elastic"`: int, Flag for saving elastic calculations (0 | 1)

`"save_elastic_file"`: string, Name of saved elastic calculation file

`"segment_file_name"`: string, Name of *_segment.csv file

`"slip_constraint_weight"`: float, Weight for segment slip constraints

`"slip_constraint_weight_max"`: float, Maximum weight for segment slip constraints (unused)

`"slip_constraint_weight_min"`: float, Minimum weight for segment slip constraints (unused)

`"slip_constraint_weight_steps"`: int, Iterations for testing segment slip constraint weights (unused)

`"slip_file_names"`: string, Names of slip constraint files (unused)

`"smooth_type"`: int, Laplacian smoothing method (unused)

`"snap_segments"`: int, Flag for snapping segments (0 | 1)

`"solution_method"`: string, Estimation method (unused)

`"solve_type"`: string, Solution type (dense | hmatrix) (but currently only tests for `"dense_no_meshes")

`"station_data_weight"`: float, Weight for GNSS velocities (unused, controlled by `"sar_weight")

`"station_data_weight_max"`: float, Maximum weight for GNSS velocities (unused)

`"station_data_weight_min"`: float, Maximum weight for GNSS velocities (unused)

`"station_data_weight_steps"`: int, Increments for GNSS velocity weight testing (unused)

`"station_file_name"`: String, Name of *_station.csv file

`"tri_con_weight"`: float, Weight of triangular slip rate constraints

`"tri_depth_tolerance"`: float, Tolerance for finding triangle depths (unused)

`"tri_edge"`: list of ints, Global flag for triangular edge constraints (unused, set in mesh parameters)

`"tri_full_coupling"`: int, Global flag for assuming full coupling on all triangles (unused)

`"tri_slip_constraint_type"`: int, Triangular slip constraint type (unused)

`"tri_slip_sign"`: list of ints, Global sign constraints for each component of triangular slip (unused)

`"tri_smooth"`: float, Global triangular smoothing weight (unused, set in mesh parameters)

`"tvr_lambda"`: float, Total Variational Regularization parameter (unused). *Flagged as unexpected after refactor*

`"unit_sigmas"`: int, Flag for forcing all data uncertainties to 1 (0 | 1)