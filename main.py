import os
import numpy as np

from src.io.density_writer import write_to_csv, get_output_file_name
from src.io.trajectory_reader import read_trajectory_file \
    , get_all_trajectory_files \
    , convert_data \
    , extract_observation_area \
    , sort_chronological \
    , extract_period_from_to \
    , calculate_pedestrian_target_distribution
from src.density.gaussian import calculate_density_timeseries
from src.density.pedestrian_count_density import calculate_pedestrian_density

INPUT_ROOT_DIRECTORY = os.path.join('input')  # directory to read imput files from
OUTPUT_ROOT_DIRECTORY = os.path.join('output')  # directory to write output files to
OBSERVATION_AREA = [0, 0, 50, 50]  # select data from observed area, [offset_x, offset_y, width, height]
TIME_STEP_BOUNDS = (10, 100)  # select data that lies between this time steps
RESOLUTION = 0.1  # resolution for density calculations
SIGMA = 0.7  # constant for gaussian density function, see `gaussian.py`
GAUSS_DENSITY_BOUNDS = (
2, 2)  # side length of quadratic area for gaussian density TODO: 1 val instead of tuple, hence symmetric


def process_data_file(file):
    # read single trajectory file
    data_raw = read_trajectory_file(file)
    #  convert to numeric data
    data_numeric = convert_data(data_raw)
    # extract data from a specified observation area
    data_observation = extract_observation_area(data_numeric, OBSERVATION_AREA)
    # sort time steps chronological
    data_chronological = sort_chronological(data_observation)
    # extract observation period
    data_period = extract_period_from_to(data_chronological, TIME_STEP_BOUNDS)
    data_reduced = []
    for time in data_period:
        if time[0][0] % 10 == 0:
            print(time[0])
            data_reduced.append(time)

    # calculate pedestrian target distribution
    pedestrian_target_distribution, global_distribution = \
        calculate_pedestrian_target_distribution(data_reduced)  # use data before it is sorted!

    return data_reduced, pedestrian_target_distribution, global_distribution


def main():
    trajectory_files = get_all_trajectory_files(INPUT_ROOT_DIRECTORY)
    number_of_files = len(trajectory_files)

    for i in range(0, number_of_files):  # process each file successively

        data_period, pedestrian_target_distribution, global_distribution = process_data_file(trajectory_files[i])
        # generate file name through pedestrian target distribution
        output_file_name = get_output_file_name(global_distribution)  # filename with global dist
        with open(OUTPUT_ROOT_DIRECTORY + output_file_name + str(i) + '.csv', mode='a') as file:
            # calculate gaussian density
            calculate_density_timeseries(data_period, OBSERVATION_AREA, \
                                         RESOLUTION, GAUSS_DENSITY_BOUNDS, SIGMA, \
                                         pedestrian_target_distribution, file)

def pedestrian_count_main():
    trajectory_files = get_all_trajectory_files(INPUT_ROOT_DIRECTORY)
    number_of_files = len(trajectory_files)
    file_name = ""
    for i in range(0, number_of_files):

        with open(OUTPUT_ROOT_DIRECTORY + file_name, mode='a') as file:
            data_period, pedestrian_target_distribution = process_data_file(trajectory_files[i])
            # calculate pedestrian target distribution
            output_file_name = get_output_file_name(pedestrian_target_distribution, name="count_density_")
            # calculate density
            calculate_pedestrian_density(data_period, OBSERVATION_AREA, 1, OUTPUT_ROOT_DIRECTORY, output_file_name, i)


main()
# pedestrian_count_main()
