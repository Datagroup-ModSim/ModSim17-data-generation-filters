import numpy as np
import math
from PIL import Image
import csv
import os
import glob

# before processing output file check attribute's column position
TIME_STEP_INDEX = 0
PED_ID_INDEX = 1
X_POS_INDEX = 2
Y_POS_INDEX = 3
VELOCITY_INDEX = 4
COUNTING_DENSITY_INDEX = 5
GAUSSIAN_DENSITY_INDEX = 6
FLOW_INDEX = 7
OVERLAPS_INDEX = 8
STRIDE_LENGTH_INDEX = 9


def convert_row(row):
    row_list = row[0].split(' ')

    # cast each col element
    timeStep = int(row_list[0])
    pedestrianId = int(row_list[1])
    x = float(row_list[2])
    y = float(row_list[3])
    # velocity = float(row_list[4])
    # countingDensity = float(row_list[5])
    # gaussianDensity = float(row_list[6])
    # flow = float(row_list[7])
    # overlaps = int(row_list[8])
    # strideLength = float(row_list[9])

    # specify output format, which cols are needed?
    return [timeStep, pedestrianId, x, y]  # velocity, countingDensity, gaussianDensity, flow, overlaps, strideLength]


def read_data(path):
    f = open(path)
    reader = csv.reader(f)
    data = []
    for row in reader:
        data.append(row)
    return data


def write_matrix_file(directory, matrix_out, timestep):
    np.savetxt(directory + str("density_ped_count{0}.csv").format(timestep), matrix_out, delimiter=';', fmt='%1.4f')


def convert_data(data):
    data = data[1:len(data)]  # remove column labels in first row
    return np.array(list(map(convert_row, data)))  # use list to evaluate mapping


def extract_area(data, x, y, width, height):
    # extract rectangular area from given scenario,
    # where x and y is the bottom left corner of observation area
    return [row for row in data if (x <= row[X_POS_INDEX] <= (x + width)) and
            (y <= row[Y_POS_INDEX] <= (y + height))]


def sort_data(data, framerate):
    end_time = int(data[-1][0])
    data_sorted = []
    for time in range(0, end_time):
        if time % framerate == 0:
            data_sorted.append(data[data[:, 0] == time, :])

    return np.array(data_sorted[1::]) # TODO fix: empty array at pos 0 after sorting


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
        matrix[h - pos[1]-1][pos[0]] = pedVal / len(positions)



# --------------------------------------------------------
# Test for density data
# --------------------------------------------------------
def test_density_data(file_dir):
    file_names = get_file_names(file_dir)

    # plot single file
    for name in file_names:
        data = read_density(file_dir + name)
        plot_density(data, file_dir, name)


def get_file_names(directory):
    os.chdir(directory)
    file_names = []

    for file in glob.glob("*.csv"):
        file_names.append(file)
    return file_names


# read data files into matrix
def read_density(file_dir):
    data = []
    with open(file_dir, 'r') as f:
        csv_reader = csv.reader(f, delimiter=';')

        for line in csv_reader:
            row = []
            for element in line:
                try:
                    row.append(float(element))
                except ValueError:
                    print(element)
            data.append(row)

    return data


def plot_density(data, file_dir, filename):
    # plot data
    data = np.array(data)
    s = data.shape
    img = Image.new('RGB', s)

    for i in range(0, s[0]):
        for j in range(0, s[1]):
            bw = np.uint8(255-255*data[i][j])

            img.putpixel((i, j), (bw, bw, bw))

    img = img.resize((s[0]*10,s[1]*10))

    img.save(str(file_dir + "{0}.png").format(filename[:-4]))


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

    test_density_data(dir_output)


main_calculation(filename_input, dir_input, dir_output, (50, 50), 1)
