import numpy as np

# before processing output file check attribute's column position
TIME_STEP_INDEX = 0
PED_ID_INDEX = 1
X_POS_INDEX = 2
Y_POS_INDEX = 3
VELOCITY_INDEX = 4
COUNTING_DENCITY_INDEX = 5
GAUSSIAN_DENCITY_INDEX = 6
FLOW_INDEX = 7
OVERLAPS_INDEX = 8
STRIDE_LENGTH_INDEX = 9

# dencity_field matrix with dencity values for ped
def calculate_gausian_dencity(ped, matrix, dencity_field, area):
    # calculate the dencity for one ped and add to matrix

    size = dencity_field.shape
    radius = int(size[0] / 2)
    origin_x = area[0][0]
    origin_y = area[0][1]
    width = area[1][0]
    height = area[1][1]
    diff_x = ped[X_POS_INDEX] - origin_x
    diff_y = ped[Y_POS_INDEX] - origin_y

    left_bound = max(0, diff_x - radius)
    right_bound = min(diff_x + radius, width - 1)
    upper_bound = min(diff_y + radius, height - 1)
    lower_bound = max(0, diff_y - radius)

    j = max(0, radius - diff_y)
    for y in range(lower_bound, upper_bound + 1):

        i = max(0, radius - diff_x)

        for x in range(left_bound, right_bound + 1):
            matrix[height - 1 - y][x] += dencity_field[size[1] - 1 - j][i]
            i += 1

        j += 1


# ----------------------------------------------------------------------


def generate_matrices(data_chron, resolution, area, dencity_field):
    size = (int(area[1][0] / resolution), int(area[1][1] / resolution))
    matrix_vec = []

    timestamp = 1
    matrix = np.zeros(size)

    for ped in data_chron:

        if ped[0] == timestamp:
            calculate_gausian_dencity(ped, matrix, dencity_field)
        else:
            matrix_vec.append(matrix)  # push
            matrix = np.zeros(size)  # neue matrix

    return matrix_vec


# ---------------------------------------------------------------------------

def gaussian(x, a, b, c):
    return a*np.exp(- (x - b) ** 2 / 2 * c ** 2)


def get_gaussian_grid(start, stop, res):
    x2 = np.arange(-1, 0, res)
    x3 = np.arange(0, 1 + res, res)
    x4 = np.append(x2, x3)
    xx, yy = np.meshgrid(x4, x4, sparse=False)

    grid = (xx ** 2 + yy ** 2) / 2
    return gaussian(grid, 1, 1, 7)

