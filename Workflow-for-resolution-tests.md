## Why resolution tests?
Slip, slip deficit, or coupling distributions along meshed faults are sensitive to model geometry, material properties, data locations, magnitude, noise, and regularization choices.  For the latter three cases, we can perform resolution tests that allow us to quantify how robust the inference of certain spatial features might be.  This step helps to minimize the possibility of a poorly constrained slip distribution being considered well-resolved.

## An example detailed workflow using a Anatolia/North Anatolian Fault model
Resolution tests are not "a run one script/notebook and you get results" type of calculation.  Rather, they are accomplished through a series of steps that provide for a great deal of flexibility.  Below are the details for a specific case using the a North Anatolian fault model as an example.

0. Create synthetic NAF slip/slip deficit distribution for resolution tests (new notebook named `NNN`)
   - Read NAF mesh geometry and boundary conditions using mesh parameters file `NNN` and triangulated geometry from `NNN`.
   - Generate synthetic slip/slip displacement vectors in multiple scenarios including but not limited to,
       - NAF completely locked.
       - NAF completely locked except for Marmara.
       - NAF completely locked except for shallow Marmara.
       - NAF completely locked except for deep Marmara.
       - NAF completely locked except for donut Marmara.
       - NAF checkerboards at various wavelengths.  The checkerboard should be a slipping/not slipping pattern.
   - Plot each of these.
   - Write each of these to either a `.npy` or `.csv` file with descriptive names.  They will be used below.

1. Generate synthetic surface velocities
    - Identify a reference block model (RBM).
        - command file name: `NNN`.
        - velocity file name: `NNN`.
        - block file name: `NNN`.
        - segment file name: `NNN`.
        - mesh parameters file name: `NNN`.
        - NAF mesh file name: `NNN`.
        - driver notebook file name: `NNN`.

    - Run RBM estimation with real data
        - Make sure to save elastic kernels with `"pickle_save": 1,`, `"save_elastic": 1,` and `"save_elastic_file": "../data/operators/*_elastic_operators.hdf5",` settings in the command file.  The latter should point to where you want to store the elastic partial derivatives.  This will ensure that the elastic kernels are saved and don't have to be recomputed for every model run.  This is valid so long as the model geometry (including meshes) do not change.  The `pickle_save` flag will store all data structures in a single pickle file that we'll reuse later.
        - Save state vector (`estimation.state_vector`) explicitly in a numpy (`.npy`) file with the name `NNN`.

    - Create a new notebook for running resolution tests named `NNN`
        - Load pickle file from RBM run.
        - Load `.npy` file with synthetic slip/slip deficit distribution for the current resolution test.
        - Construct a state vector that includes slip/slip deficit estimates.
            - Load `estimation.state_vector`.
            - Identify state vector indices associated with NAF mesh.
            - With the indices found above, set the state vector indices associated with the NAF slip elements to the values from generated in part `0`.  This is where the synthetic values are integrated into the block model.
        - Calculate noise-free synthetic velocities by doing the matrix-vector multiply between this modified state vector and the linear system operator, `estimation.operator`.
        - Add noise to synthetic surface velocities.
            - Add different realizations of Gaussian noise (including zero).
            - Add different levels Gaussian noise.
            - Write each of these sets of predicted velocities to a `*_station.csv` file.

2. Run a block model not with the real data but with the synthetic surface velocities
    - A new command file should be used here and named, `NNN`.  It should include information to reuse the previous elastic kernel with the command file flags: `"reuse_elastic": 1` and `"reuse_elastic_file": "../data/operators/*_elastic_operators.hdf5",` the latter of which should point to the output `hdf5` file produced by the model run in step 1 above.  This file contains the elastic partial derivatives.
    - The velocities for this run should be from one of the `*_station.csv` files created in step `1`.
    - Examine estimated slip deficit rates on the NAF (compare with synthetic input slip/slip deficit distribution)
        - Qualitatively (including visually) describe the extent to which the true synthetic feature are, and are not, resolved.
        - Calculate MAE and MSE between true synthetic and estimated as a function of noise level.

3. Repeat the above with various synthetic slip deficit distributions noise levels
