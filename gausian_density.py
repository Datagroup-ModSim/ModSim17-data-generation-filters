import os

import numpy as np
from density_plot_tests import test_density_data

from parse_trajectory_file import X_POS_INDEX, Y_POS_INDEX, read_data, convert_data, \
    sort_data, write_matrix_file, extract_area, get_file_names

# constants
SIGMA = 0.7  # for gaussian dist
START = 2
STOP = 2


# ----------------------------------------------------------------------
# generates a vector of matrixes each containing the density data for one timestep
# @param data trajectories
# @param resolution of the density image
# @area ((cp_x,cp_y)(width,height)) corner point of the measurement field referencing to c.sys. of complete scenario
#       and area of the measurement field
def calculate_dencity_timeseries(data, area, resolution, dist):
    size = (int(area[1][0] / resolution), int(area[1][1] / resolution))
    density_field = get_gaussian_grid(-START, STOP, resolution)

    matrix = np.zeros(size)
    index = 0
    for timestep in data:
        for ped in timestep:
            calculate_gaussian_density(ped, matrix, density_field, area, resolution)

        file_tag = str("_{0}_{1}_{2}_{3}").format(int(timestep[0][0]), \
                                        int(dist[index][0]*100), int(dist[index][1]*100),int(dist[index][2]*100))
        write_matrix_file(DIRECTORY, matrix, file_tag)  # write matrix for last timestep to file
        matrix = np.zeros(size)  # new matrix
        index+=1


# ----------------------------------------------------------------------------------------------------------------------
# density_field matrix with density values for ped calculated with static gausian density field
def calculate_gaussian_density(ped, matrix, density_field, area, resolution):
    # calculate the density for one ped and add to matrix

    size = density_field.shape
    radius = int(size[0] / 2)
    origin_x = area[0][0]
    origin_y = area[0][1]
    width = int(area[1][0] / resolution)
    height = int(area[1][1] / resolution)
    diff_x = int(
        np.round((ped[X_POS_INDEX] - origin_x) / resolution, 0))  # TODO do not round -> divide pedestrian density %
    diff_y = int(
        np.round((ped[Y_POS_INDEX] - origin_y) / resolution, 0))  # TODO do not round -> divide pedestrian density %

    left_bound = int(max(0, diff_x - radius))
    right_bound = int(min(diff_x + radius, width - 1))
    upper_bound = int(min(diff_y + radius, height - 1))
    lower_bound = int(max(0, diff_y - radius))

    j = max(0, radius - diff_y)
    for y in range(lower_bound, upper_bound + 1):

        i = max(0, radius - diff_x)
        for x in range(left_bound, right_bound + 1):
            matrix[height - 1 - y][x] += density_field[size[1] - 1 - j][i]
            i += 1

        j += 1


# ----------------------------------------------------------------------------------------------------------------------
# gaussian dist, Fromular from Wikipedia
def gaussian(x, a, b, c):
    return a * np.exp(- (x - b) ** 2 / 2 * c ** 2)


# Formular taken from BA Benedikt Zönnchen Fromular 3.9
def gaussian_distribution(p, x, sigma):
    return (1 / 2 * np.pi * sigma) * np.exp(-(np.linalg.norm(x - p) / (2 * sigma ** 2)))


def get_gaussian_grid(index1, index2, res):
    x2 = np.arange(index1, 0, res)
    x3 = np.arange(0, index2 + res, res)
    x4 = np.append(x2, x3)
    xx, yy = np.meshgrid(x4, x4, sparse=False)

    grid = np.array((xx ** 2 + yy ** 2) / 2)

    gaus = np.zeros(grid.shape)

    for i in range(0, grid.shape[0]):
        for j in range(0, grid.shape[1]):
            origin = np.zeros((1, 1))
            pos = np.array(grid[i][j])
            gaus[i][j] = gaussian_distribution(origin, pos, SIGMA)

    return np.array(gaus)


# generate a grid with descrete values for gausian density of one ped
def generate_gaussian_grid(radius):
    side = radius * 2 + 1
    grid = np.zeros((side, side))

    for i in range(0, side):
        for j in range(0, side):
            grid[i, j] = gaussian_distribution(np.array([0, 0]), np.array(np.abs([i - radius, j - radius])), SIGMA)

    return grid

def get_current_dist(sorted_data):

    distribution = []

    for timestamp in sorted_data:
        target_ids = np.array([0, 0, 0])
        num_ped = len(timestamp) # anzahl personen zum momentanen zeit schritt
        for ped in timestamp:
            if ped[4] == 1:
                target_ids[0]+=1
            elif ped[4] == 2:
                target_ids[1]+=1
            else:
                target_ids[2]+=1

        target_ids = target_ids/num_ped
        distribution.append(target_ids)

    return distribution

# ----------------------------------------------------------------------------------------------------------------------
def main_gausian_density(input_dir, area, resolution):

    t_files = get_file_names(directory=input_dir)

    for file_name in t_files:
        # read vadere output file from disk
        data_raw = read_data(file_name)

        # convert to numeric data
        data_converted = convert_data(data_raw)

        # cut area to observe
        data_area = extract_area(data_converted, area[0][0], area[0][1], area[1][0], area[1][1])

        data_sorted = sort_data(data_area, framerate=10)

        dist = get_current_dist(data_sorted)

        # calculate a vector containing a density matrix for each timestep
        calculate_dencity_timeseries(data_sorted, area, resolution, dist)

        #test_density_data(DIRECTORY, False)


#area = ((20, 5), (10, 10))
area = ((0,0),(50,50))
resolution = 0.1

DIRECTORY = os.path.join(os.path.dirname(__file__), "output\\")
INPUT_DIR = os.path.join(os.path.dirname(__file__), "input_data\\")

main_gausian_density(INPUT_DIR, area, resolution)
