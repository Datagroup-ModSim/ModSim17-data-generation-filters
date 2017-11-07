import os
import numpy as np

from src.io.density_writer import write_to_csv
from src.io.trajectory_reader import get_data_and_target_distribution
from src.density.gaussian import calc_density_timeseries

INPUT_BASE_DIR = os.path.join('input')      # directory to read imput files from
OUTPUT_BASE_DIR = os.path.join('output')    # directory to write output files to
OBSERVATION_AREA = [20, 5, 10, 10]          # select data from observed area, [offset_x, offset_y, width, height]
TIME_STEP_BOUNDS = (10, 50)                  # select data that lies between this time steps
RESOLUTION = 0.1                            # resolution for density calculations
SIGMA = 0.7                                 # constant for gaussian density function, see `gaussian.py`
GAUSS_DENSITY_BOUNDS = (1, 1)               # side length of quadratic area for gaussian density TODO: 1 val instead of tuple, hence symmetric

def main():

    #data, target_dist = get_data_and_target_distribution(INPUT_BASE_DIR, SCENARIO_COUNT, OBSERVATION_AREA)

    #timeseries = calc_density_timeseries(np.array(data), OBSERVATION_AREA, RESOLUTION, GAUSS_DENSITY_BOUNDS, SIGMA)

    #write_to_csv(OUTPUT_BASE_DIR, timeseries, target_dist)

main()
