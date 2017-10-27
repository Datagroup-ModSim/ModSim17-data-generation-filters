import csv


'''
vadere output file has following format:
timeStep | pedestrianId | x     | y     | velocity | countingDensity | gaussianDensity | flow  | overlaps | strideLength
int      | int          | float | float | float    | float           | float           | float | int      | float
'''

# output file name in the same directory as this script
##file_name='output_ts_pid.txt'
file_name = 'test.txt'

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
    return [row for row in data if (row[X_POS_INDEX] >= x and row[X_POS_INDEX] <= (x + width)) and
            (row[Y_POS_INDEX] >= y and row[Y_POS_INDEX] <= (y + height))]


def order_chronological(data):
    return sorted(data, key=lambda row: row[TIME_STEP_INDEX])
