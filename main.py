import os

from src.io.density_writer import get_output_file_name
from src.io.trajectory_reader import get_data
from src.density.gaussian_density import calculate_density_timeseries
from src.filter.filtering import filter_data

VERSION = 1.0

INPUT_DIRECTORY = os.path.join('input')  # directory to read imput files from
OUTPUT_DIRECTORY = os.path.join('output')  # directory to write output files to
INPUT_FILE_GLOB_PATTERN = ['**/*.trajectories', '**/output_ts_pid.txt']

SCENARIO_SIZE = [50,60]
OBSERVATION_AREA0 = [0, 0, 50, 60]
OBSERVATION_AREA = [20, 10, 10, 10]
OBSERVATION_AREA2 = [20, 15, 10, 10]
OBSERVATION_AREA3 = [20, 20, 10, 10]  # select data from observed area, [offset_x, offset_y, width, height]
RESOLUTION = 0.5  # resolution for density calculations
SIGMA = 0.7  # constant for gaussian density function, see `gaussian_density.py`
GAUSS_DENSITY_BOUNDS = (2, 2)  # side length of quadratic area for gaussian density TODO: 1 val instead of tuple, hence symmetric
FRAMERATE = 2
RECORDING_DENSITY_PERCENT = 80



def main():
    data = get_data(INPUT_DIRECTORY, INPUT_FILE_GLOB_PATTERN)
    density_timeseries = calculate_density_timeseries(data,\
                                                      OBSERVATION_AREA0,\
                                                      RESOLUTION,\
                                                      GAUSS_DENSITY_BOUNDS,\
                                                      SIGMA)
    data_filtered = filter_data(density_timeseries)

    #todo filter anwendung
    #todo files schreiben


    # trajectory_files = get_all_trajectory_files(INPUT_ROOT_DIRECTORY)
    # number_of_files = len(trajectory_files)
    #
    # for i in range(0, number_of_files):  # process each file successively
    #
    #     data_period, pedestrian_target_distribution, global_distribution, time_step_bounds = process_data_file(trajectory_files[i])
    #     # generate file name through pedestrian target distribution
    #     output_file_name = get_output_file_name(global_distribution)  # filename with global dist
    #     print(output_file_name)
    #     with open(OUTPUT_ROOT_DIRECTORY +'\\'+ output_file_name +"_" +str(i) + '.csv', mode='a') as file:
    #         # calculate gaussian density
    #         calculate_density_timeseries(data_period, OBSERVATION_AREA, \
    #                                      RESOLUTION, GAUSS_DENSITY_BOUNDS, SIGMA, \
    #                                      pedestrian_target_distribution, file)
    #
    #     print("done: ", str(np.round(((i+1) / number_of_files) * 100,0)), " %")
    #     print(output_file_name + str(i), " = ", trajectory_files[i])
    # # Datatype, script version tag, OBSERVATION_AREA,
    # # TIME_STEP_BOUNDS, RESOLUTION, SIGMA, GAUSS_DENSITY_BOUNDS, scenarios used
    # attributes = ["gaussian density",str(VERSION),str(SCENARIO_SIZE),\
    #               str(OBSERVATION_AREA), str(time_step_bounds), \
    #               str(RESOLUTION), str(SIGMA), str(GAUSS_DENSITY_BOUNDS),\
    #               str(FRAMERATE), str(trajectory_files).replace("input\\"," ")]
    # generate_attributes_file(OUTPUT_ROOT_DIRECTORY,attributes)
main()

def print_dist():
    trajectory_files = get_all_trajectory_files(INPUT_ROOT_DIRECTORY)
    number_of_files = len(trajectory_files)

    for i in range(0, number_of_files):  # process each file successively

        data, pedestrian_target_distribution, global_distribution, time_step_bounds = process_data_file(trajectory_files[i])
        # generate file name through pedestrian target distribution
        output_file_name = get_output_file_name(global_distribution)  # filename with global dist
        print(trajectory_files[i], " = ", global_distribution, " = ", output_file_name)

        attributes = ["gaussian density", str(VERSION), str(SCENARIO_SIZE), \
                      str(OBSERVATION_AREA), str(time_step_bounds), \
                      str(RESOLUTION), str(SIGMA), str(GAUSS_DENSITY_BOUNDS), \
                      str(FRAMERATE), str(trajectory_files).replace("input\\", " ")]
        generate_attributes_file(OUTPUT_ROOT_DIRECTORY, attributes)

def trajectories_data():
    trajectory_files = get_all_trajectory_files(INPUT_ROOT_DIRECTORY)
    number_of_files = len(trajectory_files)

    for i in range(0, number_of_files):  # process each file successively

        data, pedestrian_target_distribution, global_distribution, time_step_bounds = process_data_file(trajectory_files[i])
        # generate file name through pedestrian target distribution

        with open(OUTPUT_ROOT_DIRECTORY + '\\' + "_trajectories_" + str(i) + '.csv', mode='a') as file:
            # process trajectories data
            format_trajectories(data, file)

        # Datatype, script version tag, OBSERVATION_AREA,
        # TIME_STEP_BOUNDS, RESOLUTION, SIGMA, GAUSS_DENSITY_BOUNDS, scenarios used

    def process_data_file(file):
        # read single trajectory file
        data_raw = read_trajectory_file(file)
        #  convert to numeric data
        data_numeric = convert_data(data_raw)
        # extract data from a specified observation area
        # record only if 80% of pedestrians are inside of observation area
        data_observation = extract_observation_area(data_numeric, OBSERVATION_AREA)
        # sort time steps chronological
        data_chronological = sort_chronological(data_observation)
        # reduce data by framerate
        data_framerate = extract_framerate(data_chronological, FRAMERATE)
        data_recording_period, time_step_bounds = extract_recording_period(data_framerate, RECORDING_DENSITY_PERCENT)
        # calculate pedestrian target distribution
        pedestrian_target_distribution, global_distribution = \
            calculate_pedestrian_target_distribution(data_recording_period)  # use data before it is sorted!

        return data_recording_period, pedestrian_target_distribution, global_distribution, time_step_bounds