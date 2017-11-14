import csv
from glob import glob
import numpy as np

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

def read_trajectory_file(path):
    #print(path)
    file = open(path, newline='\n')
    file_reader = csv.reader(file, delimiter=' ')
    scenario = []
    for row in file_reader:
        scenario.append(row)
    return scenario[1:] # remove head row with labels

def convert_data(data):
    def convert_row(row):
        # cast each col element
        time_step = int(row[INDEX_TIME_STEP])
        pedestrian_id = int(row[INDEX_PED_ID])
        pos_x = float(row[INDEX_POS_X])
        pos_y = float(row[INDEX_POS_Y])
        target_id = int(row[INDEX_TARGET_ID])
        return [time_step, pedestrian_id, pos_x, pos_y, target_id]

    return list(map(convert_row, data))


def extract_observation_area(data, area):
    x = area[0]
    y = area[1]
    width = area[2]
    height = area[3]
    return ([row for row in data if (x <= row[INDEX_POS_X] <= (x + width)) and
             (y <= row[INDEX_POS_Y] <= (y + height))])


# number of targets hardcoded, currently 3
# target ids hardcoded
# also calculate total distribution
def calculate_pedestrian_target_distribution(data):
    current_dist = []
    for timestep in data:
        target_id_counts = [0, 0, 0]
        for row in timestep:
            if row[INDEX_TARGET_ID] == 4:
                target_id_counts[0] += 1
            elif row[INDEX_TARGET_ID] == 5:
                target_id_counts[1] += 1
            else:
                target_id_counts[2] += 1

        current_dist.append([round(x / len(timestep),2) for x in target_id_counts]) # TODO check if correct!

    length = len(current_dist)
    tmp = np.array(current_dist)
    print(length)
    total_dist = [np.sum(tmp[:,0]) / length, np.sum(tmp[:,1]) / length, np.sum(tmp[:,2]) / length]

    return current_dist, total_dist


def sort_chronological(data):
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

def extract_period_from_to(scenario, time_step_bounds):
    start_time_step = time_step_bounds[0]
    t_max = scenario[-1][INDEX_TIME_STEP]
    stop_time_step = t_max[0] - time_step_bounds[1]
    tmp = []
    for time_step in scenario:
        if time_step[0][INDEX_TIME_STEP] >= start_time_step and time_step[0][INDEX_TIME_STEP] <= stop_time_step:
            tmp.append(time_step)
    return tmp
