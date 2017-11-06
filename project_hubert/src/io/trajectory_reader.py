import csv
from glob import glob

################################################################################
# run with `python main.py`                                                    #
#                                                                              #
# vadere trajectories file has following format:                               #
# timeStep {int} | pedestrianId {int} | x {float} | y {float} | targetId {int} #
################################################################################

# before processing trajectories file check attribute's column position
INDEX_TIME_STEP = 0
INDEX_PED_ID = 1
INDEX_POS_X = 2
INDEX_POS_Y = 3
INDEX_TARGET_ID = 4


# Helper function to get all input file names from given root directory.
# 
# @param path: root directory to search from
def get_all_trajectory_files(root_dir):
    files = glob(root_dir + '/**/*.trajectories')
    return files


# Read vadere trajectory files recursivly from given root directory.
#
# @param path: parent directory of trajectory files
# @param nmbr_of_files: specify the number of files that are
#                       being read, if not specified all files
#                       are read
def read_trajectories(path, nmbr_of_files=-1):
    files = get_all_trajectory_files(path)
    file_count = len(files)
    scenarios = []
    if nmbr_of_files == -1:
        i_max = file_count - 1
    else:
        i_max = nmbr_of_files
    for i in range(0, i_max):
        file = open(files[i], newline='\n')
        reader = csv.reader(file, delimiter=' ')
        scenario = []
        for row in reader:
            scenario.append(row)
        scenario_without_head = scenario[1:]
        scenarios.extend(scenario_without_head)  # append for distinction between scenarios

    return scenarios


def convert_data(data):
    def convert_row(row):
        # cast each col element
        timeStep = int(row[INDEX_TIME_STEP])
        pedId = int(row[INDEX_PED_ID])
        x = float(row[INDEX_POS_X])
        y = float(row[INDEX_POS_Y])
        targetId = int(row[INDEX_TARGET_ID])
        return [timeStep, pedId, x, y, targetId]

    return list(map(convert_row, data))


def extract_observation_area(data, x, y, width, height):
    return ([row for row in data if (x <= row[INDEX_POS_X] <= (x + width)) and
             (y <= row[INDEX_POS_Y] <= (y + height))])

# number of targets hardcoded, currently 3
# target ids hardcoded
def calc_ped_target_dist(data):
    targetIdCount = [0, 0, 0]
    for ped in data:
        if ped[INDEX_TARGET_ID] == 1:
            targetIdCount[0] += 1
        elif ped[INDEX_TARGET_ID] == 2:
            targetIdCount[1] += 1
        else:
            targetIdCount[2] += 1
    return [round(x / len(data),2) for x in targetIdCount]



def sort_chron(data):
    data_sorted = sorted(data, key=lambda row:row[INDEX_TIME_STEP])
    current_time = data_sorted[0][INDEX_TIME_STEP]
    data_chron = []
    rows_equal_time = []
    for row in data_sorted:
        if row[INDEX_TIME_STEP] == current_time:
            rows_equal_time.append(row)
        else:
            data_chron.append(rows_equal_time)
            rows_equal_time = []
            rows_equal_time.append(row)
            current_time += 1
    return data_chron

def getDataAndTargetDist(path, scenario_count, area):

    # read trajectory files
    data_raw = read_trajectories(path, scenario_count)

    # convert to numeric data
    data_converted = convert_data(data_raw)

    # extract observation area
    data_observation = extract_observation_area(data_converted,
                                                area[0], area[1], area[2], area[3])
    # sort by time step
    data_chron = sort_chron(data_observation)

    # calculate target distribution
    target_dist = calc_ped_target_dist(data_observation)

    return data_chron, target_dist