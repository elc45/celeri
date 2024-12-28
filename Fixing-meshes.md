1. Convert `.msh` file to `.stl` file with modified $z$-coordinates

```python
import gmsh
import numpy as np

gmsh.initialize()
gmsh.open("cascadia.msh")

nodeTags, nodeCoords, _ = gmsh.model.mesh.getNodes()
coords = np.array(nodeCoords).reshape(-1, 3)

# Example: scale Z by 0.01
coords[:, 2] *= 0.01

for i, tag in enumerate(nodeTags):
    x, y, z = coords[i]
    gmsh.model.mesh.setNode(int(tag), [x, y, z], [])

gmsh.write("cascadia_scaled.stl")
gmsh.finalize()
```

2. Update/modify/smooth mesh with [Meshlab](https://www.meshlab.net/)

3. Convert `.stl` file back to `.msh` file with original style (km) z-coordinates

```python
import gmsh
import numpy as np

gmsh.initialize()
gmsh.open("cascadia_scaled_smoothed.stl")

nodeTags, nodeCoords, _ = gmsh.model.mesh.getNodes()
coords = np.array(nodeCoords).reshape(-1, 3)

# Example: scale Z by 0.01
coords[:, 2] /= 0.01

for i, tag in enumerate(nodeTags):
    x, y, z = coords[i]
    gmsh.model.mesh.setNode(int(tag), [x, y, z], [])
gmsh.write("cascadia_scaled_smoothed.msh")
gmsh.finalize()
```


