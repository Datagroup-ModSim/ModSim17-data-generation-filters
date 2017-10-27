#!/usr/bin/python

import csv
import numpy as np

'''
vadere output file has following format:
timeStep | pedestrianId | x     | y     | velocity | countingDensity | gaussianDensity | flow  | overlaps | strideLength
int      | int          | float | float | float    | float           | float           | float | int      | float
'''

# output file name in the same directory as this script
##file_name='output_ts_pid.txt'
file_name = 'test.txt'

# before processing output file check attribute's column position
time_step_index = 0
pedestrian_id_index = 1
x_pos_index = 2
y_pos_index = 3
velocity_index = 4
counting_density_index = 5
gaussian_density_index = 6
flow_index = 7
overlaps_index = 8
stride_length_index = 9


def convert_row(row):
    row_list = row[0].split(';')

    # cast each col element
    timeStep = int(row_list[0])
    pedestrianId = int(row_list[1])
    x = float(row_list[2])
    y = float(row_list[3])
    velocity = float(row_list[4])
    countingDensity = float(row_list[5])
    gaussianDensity = float(row_list[6])
    flow = float(row_list[7])
    overlaps = int(row_list[8])
    strideLength = float(row_list[9])

    # specify output format, which cols are needed?
    return [timeStep, pedestrianId, x, y, velocity, countingDensity, gaussianDensity, flow, overlaps, strideLength]


def read_data(path):
    f = open(path)
    reader = csv.reader(f)
    data = []
    for row in reader:
        data.append(row)
    return data


def convert_data(data):
    data = data[1:len(data)]  # remove column labels in first row
    return list(map(convert_row, data))  # use list to evaluate mapping


def extract_area(data, x, y, width, height):
    '''extract rectangular area from given scenario,
    where x and y is the bottom left corner of observation area'''
    return [row for row in data if (row[x_pos_index] >= x and row[x_pos_index] <= (x + width)) and
            (row[y_pos_index] >= y and row[y_pos_index] <= (y + height))]


def order_chronological(data):
    return sorted(data, key=lambda row: row[time_step_index])


# dencity_field matrix with dencity values for ped
def calculate_gausian_dencity(ped, matrix, dencity_field, area):
    # calculate the dencity for one ped and add to matrix

    size = dencity_field.shape
    radius = int(size[0] / 2)
    origin_x = area[0][0]
    origin_y = area[0][1]
    width = area[1][0]
    height = area[1][1]
    diff_x = ped[x_pos_index] - origin_x
    diff_y = ped[y_pos_index] - origin_y

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


def run(file_name, area, resolution, cov):

    gausian_dencity = get_gaussian_grid(5,5,0.5)

    # 1) read vadere output file from disk
    data_raw = read_data(file_name)
    # 2) convert to numeric data
    data_converted = convert_data(data_raw)
    # 3) cut area to observe
    # data_area = extract_area(data_converted, area)
    # 4) order data chronological
    data_chron = order_chronological(data_converted)
    generate_matrices(data_chron, resolution, area, gausian_dencity)



    # 5) compute density
    # 5.1) compute gaussian density
    # 5.2) compute counting density


