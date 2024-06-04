# What we want:
- Classic dense solve for Japan (multiple meshes) and WNA (simplicity)
- Nice Matplotlib visualization notebook
- Multiple solution methods: 1) Dense direct, 2) Dense iterative, 3) H-matrix, 4) Dense bounded, 5) Sparse bounded (does not exist yet), 6) Dense KL, 7) others.
- TBD

# What we have:
- `ben_hmatrix_tests.ipynb`: Contains a full direct dense solve, an iterative H-matrix solve, and an iterative dense solve. Features a clear example of linear operator preconditioning.  [demo, diagnostic, not polished but nice]

- `celeri_anatolia_eigen.ipynb`: Contains Anatolia example with classic full direct dense solve and KL solve.  Nice examples of Matplotlib graphics. [demo, diagnostic, not polished]

- `celeri_check_input.ipynb`: Contains some visual diagnostics [hacky, diagnostic, delete?]

- `celeri_dense.ipynb`: Classic full dense example. [demo]

- `celeri_dense_new.ipynb`: Classic full dense example.  Same as `celeri_dense.ipynb` except with some incomplete contourf style plotting. [demo, DELETE?]

- `celeri_hmatrix.ipynb`: Contains H-matrix example and some incomplete unbounded examples. [demo, diagnostic, not polished, DELETE?]

- `celeri_western_north_america_dense.ipynb`: Classic Western North America block model with full dense solve. [demo]

- `celeri_western_north_america_dense_experimental.ipynb`: Classic Western North America block model with *bounded* full dense solve. [demo]

- `celeri_western_north_america_dense_experimental_resolution_test.ipynb`: [TBD]

- `celeri_western_north_america_dense_tricoup.ipynb`: [TBD]

- `celeri_western_north_america_eigen.ipynb`: Western North America model with classic full dense solve and KL-eigenmode solve [demo, not polished, DELETE?]

- `celeri_western_north_america_eigen_clean.ipynb`: Western North America model with classic full dense solve and KL-eigenmode solve [demo].

- `reference_classic_tde_slip_imaging.ipynb`: Classic dense coseismic style resolution test [demo]

- `reference_dense_and_hmatrix.ipynb`: Runs a dense and H-matrix solve for Western North America.  While it runs successfully the H-matrix solution is garbage [demo, DELETE BECUASE `ben_hmatrix_tests.ipynb` WORKS?]

- `reference_fault_slip_sense.ipynb`: Documentation of standards for relative senses of fault slip.  [demo, broken but results are still in markdown table. MOVE RESULT TO DOCUMENTATION?]

- `reference_linear_operator_structure.ipynb`: A single Markdown cell showing the algebraic structure of the large linear operator. [demo, MOVE TO DOCUMENTATION?]

- `reference_map_projection_demonstration.ipynb`: Should show a single segment projected into a local coordinate frame and an elastic dislocation displacement field. [demo, BROKEN.  HISTORICALLY INTERESTING BUT DELETE?]

- `reference_pygmt.ipynb`: Shows some pygmt examples.  Not useful anymore.  [demo, DELETE?]

- `reference_sparse_dense_estimator_uncertainties.ipynb`: Small example showing equivalence of uncertainty estimates from the full covariance matrix with iterative solution from `scipy.sparse.linalg.lsqr`. [demo, DELETE?]
