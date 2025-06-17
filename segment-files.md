`*_segment.csv` files define the block model geometry.  The columns are:

`name`: Name of fault segment (string).

`lon1`: Longitude of segment endpoint 1 (float).

`lat1`: Latitude of segment endpoint 1 (float).

`lon2`: Longitude of segment endpoint 2 (float).

`lat2`: Latitude of segment endpoint 2 (float).

`dip`: Segment dip (float).  Note: May need to be flipped depending on endpoint ordering.

`create_ribbon_mesh`: Flag to determine if segment should be meshed with `segmesh.py` (int, 0 | 1, 0: don't mesh, 1: mesh).  Should this be renamed to `create_segmesh`? JPL: Yes, rename. I started to do this in celeri_ui but wanted to hold off until all naming conversions are in place. 

`locking_depth`: Segment locking depth (float).

`locking_depth_flag`: Used for replacement of locking depth with values taken from `*config.json` file (int).  I don't think this is currently in use, but it's been very useful in the past.

`ss_rate`: Soft strike-slip rate constraint value (float).

`ss_rate_sig`: Soft strike-slip rate constraint uncertainty (float).

`ss_rate_flag`: Soft strike-slip rate constraint flag (int, 0 | 1, 0: don't apply, 1: apply).

`ds_rate`:  Soft dip-slip rate constraint value (float).

`ds_rate_sig`: Soft dip-slip rate constraint uncertainty (float).

`ds_rate_flag`: Soft dip-slip rate constraint flag (int, 0 | 1, 0: don't apply, 1: apply).

`ts_rate`: Soft tensile-slip rate constraint value (float).

`ts_rate_sig`: Soft tensile-slip rate constraint uncertainty (float).

`ts_rate_flag`:  Soft tensile-slip rate constraint flag (int, 0 | 1, 0: don't apply, 1: apply).

`patch_file_name`: Index to mesh file.  (int, -1: no patch, otherwise index associated with appropriate mesh specified in `*mesh.json` file).  Per @jploveless, this should probably be renamed to something like `mesh_file_idx`: https://github.com/brendanjmeade/celeri/issues/165.

`patch_flag`: Flag to indicate that segment should be replaced by mesh (int, 0 | 1, 0: don't replace, 1: replace). Per @jploveless, this should probably be renamed to something like `mesh_file_flag`: https://github.com/brendanjmeade/celeri/issues/165.

`ss_rate_bound_flag`: Hard strike-slip rate constraint flag (int, 0 | 1, 0: don't apply, 1: apply).

`ss_rate_bound_min`: Hard strike-slip rate constraint minimum value (float).

`ss_rate_bound_max`: Hard strike-slip rate constraint maximum value (float).

`ds_rate_bound_flag`: Hard dip-slip rate constraint flag (int, 0 | 1, 0: don't apply, 1: apply).

`ds_rate_bound_min`: Hard dip-slip rate constraint minimum value (float).

`ds_rate_bound_max`: Hard dip-slip rate constraint maximum value (float).

`ts_rate_bound_flag`: Hard tensile-slip rate constraint flag (int, 0 | 1, 0: don't apply, 1: apply).

`ts_rate_bound_min`: Hard tensile-slip rate constraint minimum value (float).

`ts_rate_bound_max`: Hard tensile-slip rate constraint maximum value (float).

`rake`: slip rake orientation (float).  Currently unused.

`rake_sig`: slip rake orientation uncertainty (float).  Currently unused.

`rake_flag`: slip rake orientation flag (int, 0 | 1, 0: don't apply, 1: apply).  Currently unused.
