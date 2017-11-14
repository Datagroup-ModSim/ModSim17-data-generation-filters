import numpy as np
import os
from glob import glob
from src.tests.density_plot_tests import test_density_data, plot_gauss_glocke
from src.density.gaussian import get_gaussian_grid

# ----------------------------------------------------------------------------------------------------------------------
# this file is just for trying stuff out
# ----------------------------------------------------------------------------------------------------------------------


ped = np.array([[[1,1,4],[1,2,5],[1,3,1]], [[2,1,5],[2,3,5],[2,7,1]]])
print(ped[:,:,1])
print(np.max(ped[:,:,1]))