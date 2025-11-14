@jploveless: Need to edit this to update to reference `segmesh.py` instead of notebook

## Creating meshes from segment file elements
Segments tagged with `create_ribbon_mesh` > 0 can be meshed into continuous networks of triangular dislocation elements, termed ribbon meshes, using the notebook [`segment_meshing.ipynb`](https://github.com/brendanjmeade/celeri/blob/main/notebooks/segment_meshing.ipynb). This flag can be specified within a segment file, and the meshing takes place after the block closure routine so that the segments can be properly ordered. 

First, the bottom coordinates of each segment are found, reckoning from the endpoints in a direction perpendicular to strike by the horizontal projection of the fault width; this is zero for vertical segments. Along a contiguous subset of segments, the bottom coordinates are averaged so that a closed loop of top and bottom vertices can be constructed. This means that, when adjacent segments differ in dip and/or locking depth, the originally specified segment properties do not strictly propagate into the TDE mesh. Geometric consequences include trapezoidal faults (where adjacent segments have different locking depths) and modification of specified dip. Creating shorter segments, including through repeated splitting to retain consistent properties, can reduce the impact of the bottom coordinate averaging. 

Meshing is carried out using [`Gmsh`](https://gmsh.info), and specifically using several features. First, each segment (with averaged bottom coordinates) is specified as its own quadrilateral surface, but these surfaces are merged to create a compound surface ([`gmsh.model.mesh.setCompound`](https://gmsh.info/doc/texinfo/gmsh.html#index-gmsh_002fmodel_002fmesh_002fsetCompound)). The original surfaces are generated using [`gmsh.model.geo.addSurfaceFilling`](https://gmsh.info/doc/texinfo/gmsh.html#index-gmsh_002fmodel_002fgeo_002faddSurfaceFilling) rather than [`gmsh.model.geo.addPlaneSurface`](https://gmsh.info/doc/texinfo/gmsh.html#index-gmsh_002fmodel_002fgeo_002faddPlaneSurface), which produced nonplanar surfaces in testing. 

Meshing is carried out using geocentric Cartesian coordinates, but the TDE nodes are converted back to longitude, latitude, depth (km) coordinates before being written to a `.msh` file. A unique `.msh` file is written for each set of contiguous segments as `(segment_file_name)_ribbonmesh1.msh`, `(segment_file_name)_ribbonmesh2.msh`, etc. using the same folder as any originally specified meshes. We start with `..._ribbonmesh1.msh` rather than `..._ribbonmesh0.msh` so that the numerical index can correspond to an updated `create_ribbon_mesh` flag in the segment file. 

In addition to generating the meshes, the ribbon meshing routine updates several Dicts and DataFrames, which are written to updated files for use in a subsequent `celeri` run: 
- In `Segment`, `patch_file_name` is set to be a new integer corresponding to the ribbon mesh index (corrected for number of meshes in the original `.mshp` file), and `patch_flag` is set to 1. This allows the locking depth of the segment to be set to zero. `create_ribbon_mesh` is set to zero so that meshes are not recreated. 
- The `.mshp` file is updated with new entries identifying the newly created ribbon meshes. These are added after any existing meshes and the listing order corresponds to the values in `segment.patch_file_name`.
- A new `.command` file is written, updated with the filenames of the new `segment.csv` and mesh parameter `.json` files. These are placed in the same folder as the original files, with `_ribbonmesh` appended.

## Using celeri-segmesh
1. Modify `<segment.csv>` file so that `create_ribbon_mesh = 1` for all segments that you want meshed.  Make sure that a `<config.json>` file points to this `<segment.csv>` file.
2. Call segmesh.  For example: `celeri-segmesh data/config/wna_config.json -el 2 8`.  The `-el 2 8` part sets a meshing target 2 km element spacing at the top of the mesh and 8 km at the bottom.
3. This produces (and will clobber) updated model files:
  - Creates `*_segmesh.csv`: Updated segment file with mesh flags set
  - Creates `*_segmesh.json`: Updated config file referencing new meshes
  - Creates `*mesh_params_segmesh.json`: Mesh parameter file
  - Creates `.msh` files in your mesh directory

## Creating "Base of elastic layer" (BEL) meshes
1. Create a `<polygon.csv>` file with lon and lat coordinates of an approximate geographic polygon representing the BEL region.
2. Run `python create_bel_mesh_from_poly.py <polygon.csv> <buffer> <depth> <mesh spacing>`
   - `<buffer>`: Length scale (approximate km) to create a smooth outer buffer of the initial polygon using shapely
   - `<depth>`: Depth of BEL (km).  Should be a positive number but is converted to negative when writing the output `.msh` file.
   - `<mesh spacing>`: Approximate spacing of mesh elements (approximate km)
