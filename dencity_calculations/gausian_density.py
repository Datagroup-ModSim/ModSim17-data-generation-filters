import numpy as np
from dencity_calculations.parse_trajectory_file import X_POS_INDEX, Y_POS_INDEX, read_data, convert_data, write_to_file, \
    sort_data

dir = "R:\\IC7\\ModelierungsSeminar\\data-generation-filters\\ModSim17-data-generation-filters\\output\\"


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
        ped[X_POS_INDEX]) / resolution - origin_x  # TODO do not cast to int -> divide pedestrian density proportionally
    diff_y = int(
        ped[Y_POS_INDEX]) / resolution - origin_y  # TODO do not cast to int -> divide pedestrian density proportionally

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


# ----------------------------------------------------------------------
# generates a vector of matrixes each containing the density data for one timestep
# @param data trajectories
# @param resolution of the density image
# @area ((cp_x,cp_y)(width,height)) corner point of the measurement field referencing to c.sys. of complete scenario
#       and area of the measurement field

def generate_matrices(data, resolution, area):
    size = (int(area[1][0] / resolution), int(area[1][1] / resolution))
    matrix_vec = []

    timestamp = 1
    matrix = np.zeros(size)

    density_field = generate_gaussian_grid(radius=2)

    for ped in data:

        if ped[0] == timestamp:
            calculate_gaussian_density(ped, matrix, density_field, area, resolution)
        elif (ped[0]) == (timestamp + 1):  # next timestamp
            matrix_vec.append(matrix)
            matrix = np.zeros(size)  # neue matrix
            calculate_gaussian_density(ped, matrix, density_field, area, resolution)
            timestamp += 1

    matrix_vec.append(matrix)  # append last time step

    return matrix_vec


# ---------------------------------------------------------------------------

# gaussian dist, Fromular from Wikipedia
def gaussian(x, a, b, c):
    return a * np.exp(- (x - b) ** 2 / 2 * c ** 2)


# Formular taken from BA Benedikt Zönnchen Fromular 3.9
def gaussian_distribution(p, x, sigma):
    return (1 / 2 * np.pi * sigma) * np.exp(-(np.linalg.norm(x - p) / (2 * sigma ** 2)))


# generate a grid with descrete values for gausian density of one ped
def generate_gaussian_grid(radius):
    side = radius * 2 + 1
    grid = np.zeros((side, side))

    for i in range(0, side):
        for j in range(0, side):
            grid[i, j] = gaussian_distribution(np.array([0, 0]), np.array(np.abs([i - radius, j - radius])), sigma=0.7)

    return grid


def main_gausian_density(file_name, area, resolution):
    # gasian_density = get_gaussian_grid(5, 5, 0.5)

    # read vadere output file from disk

    data_raw = read_data(file_name)

    # convert to numeric data
    data_converted = convert_data(data_raw)

    # cut area to observe
    # data_area = extract_area(data_converted, area)

    # calculate a vector containing a density matrix for each timestep
    density_time_series = generate_matrices(data_converted, resolution, area)

    write_to_file(density_time_series)


    # 5) compute density
    # 5.1) compute gaussian density
    # 5.2) compute counting density


area = ((0, 0), (50, 50))
resolution = 0.1
file = "R:\\IC7\\ModelierungsSeminar\\data-generation-filters\\ModSim17-data-generation-filters\\testdata\\test.txt"
main_gausian_density(file, area, resolution)
