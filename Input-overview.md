`celeri` models interpret geodetic velocity fields as arising from crustal block rotations, elastic strain accumulation on partially to fully coupled faults that bound the blocks, homogeneous strain within crustal blocks, and Mogi sources representing magma chamber volume changes. Input files define the constraining geodetic data, crustal fault and block geometry, and Mogi sources. 

- `*config.json` (previously `*command.json`) holds geodetic observations, locations, and velocities.
- `*station.csv` holds geodetic observations, locations, and velocities.
- `*segment.csv` contains two endpoints of each rectangular fault segment comprising the model geometry, along with locking depth (depth below the surface to which the fault is assumed to be coupled during the nominal interseismic period) and dip. _A priori_ slip rates can also be specified within this file. 
- `*block.csv` contains an "interior point" for each crustal block. The fault segments themselves define continuous polygons, each of which contains an interior point. _A priori_ rotation rates, specified as Euler poles, can be included in this file, as well as a flag indicating whether internal strain rates should be estimated. 
- `*mogi.csv` (optional) defines Mogi source geometry using latitude, longitude, and depth. 
- `*mesh_param.json` (optional) describes parameters related to meshes of triangular dislocation elements (TDEs) that can be used to represent more geometrically complex fault surfaces, such as subduction zone interfaces. The mesh parameters include references to `.msh` files, created with Gmsh, that define networks of TDEs in latitude (degrees), longitude (degrees), depth (km) space. 

