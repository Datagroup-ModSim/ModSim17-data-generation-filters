import csv
import numpy as np

# @author Rebecca Brydon / Lisa Grundman

# ----------------------------------------------------------------------------------------------------------------------
# Voronoi density
# ----------------------------------------------------------------------------------------------------------------------

# TODO voroni density

# ----------------------------------------------------------------------------------------------------------------------
# Pedestrian count density
# ----------------------------------------------------------------------------------------------------------------------

# counts pedestrian density in units
# @param data_chron chronologically sorted pedestrian data
# @param size of measurement_field
# @param framerate in which density images should be calculated

def count_ped_density(data_chron, size, framerate):

    # save list of matrixes, every matrix contains density data for one timestep / or framerate
    matrix_list = []

    timestamp = 1
    end_timestamp = data_chron[-1][0] # get last time stamp
    matrix = np.zeros(size)

    for ped in data_chron:

        if ped[0] == timestamp:
            calculate_density(ped, matrix)

        else:
            matrix_list.append(matrix)  # push
            matrix = np.zeros(size)  # neue matrix

    return matrix_list


def calculate_density(ped, matrix):

    print("DOTO")
    # check if split ped

    # add density values to matrix

