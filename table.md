Generated using pyGCS (Grid Convergence Study)
- https://github.com/tomrobin-teschner/pyGCS
- https://pypi.org/project/pygcs/

Table 1: Grid convergence study over 3 grids. phi represents the {INSERT MEANING OF PHI HERE} and phi_extrapolated its extrapolated value. N_cells is the number of grid elements, r the refinement ration between two successive grids. GCI is the grid convergence index in percent and its asymptotic value is provided by GCI_asymptotic, where a value close to unity indicates a grid independent solution. The order achieved in the simulation is given by p.

|        |  phi      |   N_cells   |  r  |  GCI  | GCI_asymptotic |  p   | phi_extrapolated |
|--------|:---------:|:-----------:|:---:|:-----:|:--------------:|:----:|:----------------:|
|        |           |             |     |       |                |      |                  |
| Grid 1 | 6.063e+00 |     2465237 | 1.2 | 2.11% |                |      |                  |
| Grid 2 | 5.972e+00 |     1368606 | 1.4 | 1.13% |      0.284     | 3.25 |     6.17e+00     |
| Grid 3 | 5.863e+00 |      493360 | -   | -     |                |      |                  |
|        |           |             |     |       |                |      |                  |