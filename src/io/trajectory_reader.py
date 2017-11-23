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


# converts the read data from strings to numeric data
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


# extracts the observation area of the camera from the data
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
            if row[INDEX_TARGET_ID] == 4: # TODO read target id tags from file
                target_id_counts[0] += 1
            elif row[INDEX_TARGET_ID] == 5:
                target_id_counts[1] += 1
            else:
                target_id_counts[2] += 1

        current_dist.append([round(x / len(timestep),2) for x in target_id_counts]) # TODO check if correct!

    #current_dist = list(map(map_to_100_percent,current_dist))

    length = len(current_dist)
    tmp = np.array(current_dist)
    total_dist = [np.sum(tmp[:,0]) / length, np.sum(tmp[:,1]) / length, np.sum(tmp[:,2]) / length]

    #total_dist = map_to_100_percent(total_dist)

    if not np.sum(total_dist) == 1.0: # TODO check mapping
        print(total_dist)
        #raise ValueError("Distribution dose not add up to 100%!")

    return current_dist, total_dist

# Helper method for mapping non 100% distributions to the correct scale
def map_to_100_percent(dist):
    dist = np.round(dist,2)
    factor = 1 / np.sum(dist)
    dist = np.round([dist[0] * factor, dist[1] * factor, dist[2] * factor],2)
    return dist

# sorts the data chronologicaly by timestep
# new format: [[list of all data for timestep 1], [list of all data for timestep 2], [...], ... ]
def sort_chronological(data):
    print("length: ",len(data))
    data_sorted = sorted(data, key=lambda row:row[INDEX_TIME_STEP])
    current_time = data_sorted[0][INDEX_TIME_STEP]
    data_chron = []
    rows_equal_time = []
    chron_len = 0
    for row in data_sorted:
        if row[INDEX_TIME_STEP] == current_time:
            rows_equal_time.append(row)
        else:
            data_chron.append(rows_equal_time)
            chron_len = chron_len + len(rows_equal_time)
            rows_equal_time = []
            rows_equal_time.append(row)
            current_time += 1

    return data_chron

# reduces data
# takes only every "framerate" timestep
def extract_framerate(data, framerate):
    data_reduced = []
    for time in data:
        if time[0][0] % framerate == 0:
            data_reduced.append(time)

    return data_reduced


# record only if a given percent of pedestrians are already inside the observation area for the camera
# @param data trajectory data sorted by timestep
# @param percent percentage of how full the observation area should at least be before starting to record
def extract_recording_period(data, percent):
    tmp = [len(timestep) for timestep in data]
    max_length_timestep = np.max(tmp)
    length_boundary = int((max_length_timestep*percent)/100)
    recording = []
    for timestep in data:
        if len(timestep) >= length_boundary:
            recording.append(timestep)

    return recording


# currently not in use anymore
# cuts out the given time period
def extract_period_from_to(scenario, time_step_bounds):
    start_time_step = time_step_bounds[0]
    #t_max = scenario[-1][INDEX_TIME_STEP]
    stop_time_step = time_step_bounds[1]
    tmp = []
    for time_step in scenario:
        if time_step[0][INDEX_TIME_STEP] >= start_time_step and time_step[0][INDEX_TIME_STEP] <= stop_time_step:
            tmp.append(time_step)
    return tmp
