import math

import numpy as np
from density_plot_tests import test_density_data

from parse_trajectory_file import write_matrix_file, X_POS_INDEX, Y_POS_INDEX, \
    read_data, convert_data, sort_data


# ----------------------------------------------------------------------------------------------------------------------
# Pedestrian count density
# ----------------------------------------------------------------------------------------------------------------------

# counts pedestrian density in units
# @param data chronologically sorted pedestrian data by time step
# @param size of measurement_field
def count_ped_density(data, size_measurement_field, resolution, dir_output):
    size_matrix = (int(size_measurement_field[0] / resolution), int(size_measurement_field[0] / resolution))

    for timestep in data:  # iterate over pedestrians
        matrix = np.zeros(size_matrix)  # new matrix for new time step
        for ped in timestep:
            find_density_distribution(ped, matrix, resolution)

        write_matrix_file(dir_output, matrix, timestep[0][0])  # write matrix directly to file


# add density of ped depending on current possition
def find_density_distribution(ped, matrix, resolution):
    x_pos = np.round(ped[X_POS_INDEX] / resolution, 1)  # round to 1 numb after decimal point
    y_pos = np.round(ped[Y_POS_INDEX] / resolution, 1)

    x_pos_frac, x_pos_int = math.modf(x_pos)
    y_pos_frac, y_pos_int = math.modf(y_pos)

    x_pos_int = int(x_pos_int)
    y_pos_int = int(y_pos_int)

    h = matrix.shape[1]

    pedVal = 1

    positions = []
    if x_pos_frac != 0 and y_pos_frac != 0:  # ped is only standing with in one field
        positions.append([x_pos_int, y_pos_int])
    else:  # border cases
        positions.append([x_pos_int, y_pos_int])  # at least current must added
        if x_pos_frac == 0:  # ped standing between two fields on x-axis
            if y_pos_frac == 0:  # ped standing between two fields on y-axis
                # check if coordinates are valid
                if x_pos_int > 0:
                    positions.append([x_pos_int - 1, y_pos_int])  # field to the left of ped
                    if y_pos_int > 0:
                        positions.append([x_pos_int, y_pos_int - 1])  # field below ped
                        positions.append([x_pos_int - 1, y_pos_int - 1])  # field diagonal from ped

            else:  # only between two field on x-axis
                positions.append([x_pos_int - 1, y_pos_int])
        else:  # only between two field on y-axis
            positions.append([x_pos_int, y_pos_int - 1])

    for pos in positions:
        matrix[h - pos[1] - 1][pos[0]] = pedVal / len(positions)



# -------------------------------------------------------------------------------------------------

dir_output = "R:\\IC7\\ModelierungsSeminar\\data-generation-filters\\ModSim17-data-generation-filters\\output\\"
dir_input = "R:\\IC7\\ModelierungsSeminar\\data-generation-filters\\ModSim17-data-generation-filters\\testdata\\"
filename_input = "postvis.trajectories"


def main_calculation(filename, dir_input, dir_output, size_measurement_field, resolution):
    data_raw = read_data(dir_input + filename)
    data = convert_data(data_raw)

    # sort data by time step, only take the wanted time steps
    data_sorted = sort_data(data, framerate=10)

    # calculate ...
    count_ped_density(data_sorted, size_measurement_field, resolution, dir_output)

    test_density_data(dir_output, resize=True)


main_calculation(filename_input, dir_input, dir_output, (50, 50), 1)
