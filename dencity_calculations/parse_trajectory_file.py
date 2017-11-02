import csv
import numpy as np

'''
vadere output file has following format:
timeStep | pedestrianId | x     | y     | velocity | countingDensity | gaussianDensity | flow  | overlaps | strideLength
int      | int          | float | float | float    | float           | float           | float | int      | float
'''

# output file name in the same directory as this script
# file_name='output_ts_pid.txt'
# file_name = 'test.txt'

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


def convert_row(row):
    row_list = row[0].split(' ')

    # cast each col element
    timeStep = int(row_list[0])
    pedestrianId = int(row_list[1])
    x = float(row_list[2])
    y = float(row_list[3])
    targetID = int(row_list[4])
    # velocity = float(row_list[4])
    # countingDensity = float(row_list[5])
    # gaussianDensity = float(row_list[6])
    # flow = float(row_list[7])
    # overlaps = int(row_list[8])
    # strideLength = float(row_list[9])

    # specify output format, which cols are needed?
    return [timeStep, pedestrianId, x, y, targetID]  # , velocity, countingDensity, gaussianDensity, flow, overlaps, strideLength]


def read_data(path):
    f = open(path)
    reader = csv.reader(f)
    data = []
    for row in reader:
        data.append(row)
    return data


def write_matrix_file(directory, matrix_out, timestep):
    np.savetxt(directory + str("density_ped_count{0}.csv").format(timestep), matrix_out, delimiter=';', fmt='%1.4f')


def write_to_file(data_vec):
    timestep = 1
    for data in data_vec:
        np.savetxt(dir + str("density{0}.csv").format(timestep), data, delimiter=';', fmt='%1.4f')

        ++timestep


def convert_data(data):
    data = data[1:len(data)]  # remove column labels in first row
    return np.array(list(map(convert_row, data)))  # use list to evaluate mapping


def extract_area(data, x, y, width, height):
    # extract rectangular area from given scenario,
    # where x and y is the bottom left corner of observation area
    return np.array([row for row in data if (x <= row[X_POS_INDEX] <= (x + width)) and
     (y <= row[Y_POS_INDEX] <= (y + height))])


def sort_data(data, framerate):
    end_time = int(data[-1][0])
    data_sorted = []
    targets = list(set(data[:, 4]))
    distribution = []
    for time in range(0, end_time):
        if time % framerate == 0:
            data_sorted.append(data[data[:, 0] == time, :])
            tmp = data[data[:, 0] == time, 4]
            current = []
            for target in range(0, len(targets)):
                current.append((tmp == targets[target]).sum()/len(tmp))
            distribution.append(current)
    return np.array(data_sorted[1::]), distribution[1:]  # TODO fix: empty array at pos 0 after sorting


def order_chronological(data):
    return sorted(data, key=lambda row: row[TIME_STEP_INDEX])
