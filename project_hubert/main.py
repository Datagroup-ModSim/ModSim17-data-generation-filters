import os
import numpy as np

from src.io.trajectory_reader import getDataAndTargetDist
from src.density.gaussian import calc_density_timeseries
from src.io.density_writer import write_to_csv

INPUT_BASE_DIR = os.path.join('input')
OUTPUT_BASE_DIR = os.path.join('output')
OBSERVATION_AREA = [20, 5, 10, 10]
SCENARIO_COUNT = 1
RESOLUTION = 0.1
SIGMA = 0.7
GAUSS_DENSITY_BOUNDS = (1, 1)

def main():

    data, target_dist = getDataAndTargetDist(INPUT_BASE_DIR, SCENARIO_COUNT, OBSERVATION_AREA)

    timeseries = calc_density_timeseries(np.array(data), OBSERVATION_AREA, RESOLUTION, GAUSS_DENSITY_BOUNDS, SIGMA)

    write_to_csv(OUTPUT_BASE_DIR, timeseries, target_dist)

main()
