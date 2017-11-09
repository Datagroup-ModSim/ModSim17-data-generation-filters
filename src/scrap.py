import numpy as np
import os
from glob import glob
from src.tests.density_plot_tests import test_density_data, plot_gauss_glocke
from src.density.gaussian import get_gaussian_grid

# ----------------------------------------------------------------------------------------------------------------------
# this file is just for trying stuff out
# ----------------------------------------------------------------------------------------------------------------------

INPUT_BASE_DIR = "R:\\IC7\\ModelierungsSeminar\\data-generation-filters\\ModSim17-data-generation-filters\\vadere_gaussdichte\\"


def do_some_thing(index, file):
    file.write(str(index)+'\n')
    file.flush()


with open("test_file.csv",mode='a') as f:
    for i in range(0,10):
        do_some_thing(i,f)

    print("finished")


