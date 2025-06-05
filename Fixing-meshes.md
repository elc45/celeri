Some meshes require cleaning to remove redundant and ill-shaped elements.  Meshlab is fantastic for visualizing and fixing meshes but doesn't support the .msh format.  The basic workflow for this is:

1. Convert `.msh` file to `.stl` using the [`msh2stl.py`](https://github.com/brendanjmeade/celeri/blob/main/celeri/scripts/msh2stl.py) script (with modified (unphysical pseudo-degrees) $z$-coordinates)
2. Load `.stl` file into Meshlab
3. Update/modify/smooth mesh with [Meshlab](https://www.meshlab.net/)
4. Save the modified .stl file from Meshlab
5. Convert `.stl` to `.msh` file with [`stl2msh.py`](https://github.com/brendanjmeade/celeri/blob/main/celeri/scripts/stl2msh.py) (with unprojection from modified (unphysical pseudo-degrees) $z$-coordinates)
