import numpy as np
import os
from glob import glob
from src.tests.density_plot_tests import test_density_data, plot_gauss_glocke
from src.density.gaussian import get_gaussian_grid

# ----------------------------------------------------------------------------------------------------------------------
# this file is just for trying stuff out
# ----------------------------------------------------------------------------------------------------------------------

INPUT_BASE_DIR = "R:\\IC7\\ModelierungsSeminar\\data-generation-filters\\ModSim17-data-generation-filters\\vadere_gaussdichte\\"
#test_density_data(INPUT_BASE_DIR, resize=False)

grid = get_gaussian_grid(1,1,0.05,0.7)
print(np.shape(grid))
plot_gauss_glocke(grid)

