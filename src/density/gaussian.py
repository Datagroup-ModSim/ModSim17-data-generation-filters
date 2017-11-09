import numpy as np
from src.tests.density_plot_tests import read_density
from src.io.density_writer import write_matrix_to_file

INDEX_TIME_STEP = 0
INDEX_PED_ID = 1
INDEX_POS_X = 2
INDEX_POS_Y = 3
INDEX_TARGET_ID = 4


def gaussian_pdf(ped_rad, sigma, x):
    norm = np.linalg.norm(x - ped_rad)
    nenner = ((0.195*2)**2)*np.sqrt(3)*0.5
    zaehler = (2*np.pi*sigma**2)
    factor = np.sqrt(nenner/zaehler)

    return factor*(1 / 2 * np.pi * sigma) * np.exp(-norm / (2 * sigma ** 2))

def get_gaussian_grid(start, stop, res, sigma):
    x1 = np.arange(-start, 0, res)
    x2 = np.arange(0, stop + res, res)
    x = np.append(x1, x2)
    xx, yy = np.meshgrid(x, x, sparse=False)
    grid = (xx ** 2 + yy ** 2) # / ((stop ** 2) * 2)
    ped_radius = np.zeros([1,1])
    gauss = np.vectorize(gaussian_pdf)
    return gauss(ped_radius, sigma, grid)

def get_vadere_gaussian_grid():
    data = read_density("vadere_gaussian.csv")
    return np.array(data)


    # ----------------------------------------------------------------------------------------------------------------------
    # density_field matrix with density values for ped calculated with static gausian density field
def add_pedestrian_density(ped, matrix, density_field, area, resolution):
    # calculate the density for one ped and add to matrix

    size = density_field.shape
    radius = int(size[0] / 2)
    origin_x = area[0]
    origin_y = area[1]
    width = int(area[2] / resolution)
    height = int(area[3] / resolution)
    diff_x = int(
        np.round((ped[INDEX_POS_X] - origin_x) / resolution, 0))  # TODO do not round -> divide pedestrian density %
    diff_y = int(
        np.round((ped[INDEX_POS_Y] - origin_y) / resolution, 0))  # TODO do not round -> divide pedestrian density %

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

    return matrix

# ----------------------------------------------------------------------
# generates a vector of matrixes each containing the density data for one timestep
# @param data trajectories
# @param resolution of the density image
# @area ((cp_x,cp_y)(width,height)) corner point of the measurement field referencing to c.sys. of complete scenario
#       and area of the measurement field
def calculate_density_timeseries(data, area, resolution, bounds, sigma, current_dist, file):

    size = (int(area[2] / resolution), int(area[3] / resolution))
    density_field = get_gaussian_grid(bounds[0], bounds[1], resolution, sigma)
    #density_field = get_vadere_gaussian_grid()

    matrix = np.zeros(size)
    print(size)
    index = 0
    for timestep in data:
        for ped in timestep:
            add_pedestrian_density(ped, matrix, density_field, area, resolution)

        write_matrix_to_file(matrix, current_dist[index],file)
        matrix = np.zeros(size)  # new matrix
        index += 1
