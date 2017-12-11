from src.io.file_reader import FileReader
from src.io.file_writer import create_output_directory, write_density_timeseries, write_trajectories_formatted, \
    generate_attributes_file_density, generate_attributes_file_trajectories
from src.density.gaussian_density import calculate_density_timeseries

from src.trajectories.trajectories_formatter import format_trajectories

from src.util.helper import calculate_total_target_distribution, calculate_momentary_target_distributions
from src.filter.pca import mainPCA
import os

VERSION = 1.1

INPUT_DIRECTORY = os.path.join('input')  # directory to read imput files from
OUTPUT_DIRECTORY = os.path.join('output')  # directory to write output files to
INPUT_FILE_GLOB_PATTERN = ['/**/**/*.trajectories', '**/output_ts_pid.txt']
SCENARIO_SIZE = [50,60]
# select data from observed area, [offset_x, offset_y, width, height]
OBSERVATION_AREA0 = [0, 0, 50, 60]
OBSERVATION_AREA1 = [20, 10, 10, 10]
OBSERVATION_AREA2 = [20, 15, 10, 10]
OBSERVATION_AREA3 = [20, 20, 10, 10]
RESOLUTION = 0.5  # resolution for density calculations
SIGMA = 0.7  # constant for gaussian density function, see `gaussian_density.py`
GAUSS_DENSITY_BOUNDS = (2, 2)
FRAMERATE = 2
RECORDING_DENSITY_PERCENT = 80
CALCULATE_VELOCITY = False


def run_density_calculations(observation_area, sub_output_folder):
    unique_id = 0
    trajectory_reader = FileReader(INPUT_DIRECTORY, INPUT_FILE_GLOB_PATTERN)
    while not trajectory_reader.is_finished:
        data, current_input_directory = trajectory_reader.get_next_data(observation_area,
                                                                        FRAMERATE,
                                                                        RECORDING_DENSITY_PERCENT,
                                                                        CALCULATE_VELOCITY)

        current_output_directory = create_output_directory(current_input_directory, OUTPUT_DIRECTORY)

        density_timeseries = calculate_density_timeseries(data, observation_area, RESOLUTION,
                                                          GAUSS_DENSITY_BOUNDS, SIGMA)

        #density_timeserie_filtered = filter_data(density_timeseries)

        #density_timeseries = mainPCA(density_timeseries)

        total_target_distribution = calculate_total_target_distribution(data)

        momentary_target_distributions = calculate_momentary_target_distributions(data)

        unique_id = write_density_timeseries(density_timeseries, sub_output_folder,
                                             total_target_distribution, momentary_target_distributions,
                                             unique_id)

    density_constants = [RESOLUTION, SIGMA, GAUSS_DENSITY_BOUNDS, FRAMERATE]
    generate_attributes_file_density(trajectory_reader.input_file_names,observation_area, sub_output_folder, SCENARIO_SIZE, density_constants)


# files_used,observation_area, output_path, scenario_size, section_density_values
def run_trajectories_formatter(observation_area):

    unique_id = 0
    trajectory_reader = FileReader(INPUT_DIRECTORY, INPUT_FILE_GLOB_PATTERN)

    while not trajectory_reader.is_finished:
        data, current_input_directory = trajectory_reader.get_next_data(observation_area, FRAMERATE, RECORDING_DENSITY_PERCENT)
        current_output_directory = create_output_directory(current_input_directory, OUTPUT_DIRECTORY)
        trajectory_formatted = format_trajectories(data, observation_area)
        unique_id = write_trajectories_formatted(trajectory_formatted, current_output_directory, unique_id)

    # generate_attributes_file_density(trajectory_reader.input_file_names,OBSERVATION_AREA, OUTPUT_DIRECTORY, SCENARIO_SIZE, density_constants)


# ----------------------------------------------------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------------------------------------------------

observation_areas = [OBSERVATION_AREA0]

folders = os.listdir(INPUT_DIRECTORY)
print(folders)
tags = "pos{0}"

for folder in folders:
    ped_count = folder[0:3]

    for i in range(0, len(observation_areas)):
        output_folder_name = ped_count + "_" + tags.format(i+1)
        sub_output_folder = os.path.join(OUTPUT_DIRECTORY, output_folder_name)
        os.makedirs(sub_output_folder)
        run_density_calculations(observation_areas[i], sub_output_folder)

