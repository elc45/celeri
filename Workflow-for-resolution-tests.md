## Why resolution tests?
Slip, slip deficit, or coupling distributions along meshed faults are sensitive to model geometry, material properties, data locations, magnitude, noise, and regularization choices.  For the latter three cases, we can perform resolution tests that allow us to quantify how robust the inference of certain spatial features might be.  This step helps to minimize the possibility of a poorly constrained slip distribution being considered well-resolved.

## An example detailed workflow using a North Anatolian Fault
Resolution tests are not "a run one script/notebook and you get results" type of calculation.  Rather, they are accomplished through a series of steps that provide for a great deal of flexibility.  Below are the details for a specific case using the a North Anatolian fault model as an example

0. Create synthetic NAF slip/slip deficit distribution for resolution tests (new notebook named `NNN`)
   - Read NAF mesh geometry and boundary conditions using mesh parameters file `NNN` and triangulated geometry from `NNN`.

1. Generate synthetic surface velocities
    - Identify a reference block model.
        - command file name: `NNN`
        - velocity file name: `NNN`
        - block file name: `NNN`
        - segment file name: `NNN`
        - mesh parameters file name: `NNN`
        - NAF mesh file name: `NNN`
        - driver notebook file name: `NNN`

    - Run an inverse block model with real data
        - Take block motions from the state vector
        - Construct a new state vector with the estimated block motions and a new NAF slip deficit distribution.  This becomes the known truth that we want to estimate
    - Take state vector and synthetic state vector to predict noise-free synthetic velocities
    - Add noise to synthetic surface velocities
2. Run a block model not with the real data but with the synthetic surface velocities.
    - These should be stored as a `.csv` file, just like a regular velocity file.
    - Systematically document how well the synthetic NAF slip deficit distribution can be inferred.  We have a synthetic truth here, so we can quantify this exactly!
3. Repeat the above with various synthetic slip deficit distributions, including (but not limited to):
    - NAF completely locked
    - NAF completely locked except for Marmara
    - NAF completely locked except for shallow Marmara
    - NAF completely locked except for deep Marmara
    - NAF completely locked except for donut Marmara
    - NAF checkerboards at various resolutions (not because it's informative but because reviewers always ask for this)