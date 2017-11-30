INDEX_TIME_STEP = 0
INDEX_PEDESTRIAN_ID = 1
INDEX_POSITION_X = 2
INDEX_POSITION_Y = 3
INDEX_TARGET_ID = 4
INDEX_VELOCITY_ABSOULTE = 5
INDEX_VELOCITY_X = 6
INDEX_VELOCITY_Y = 7

def sort_by(data, key):
    """
    Sort data by given criteria.

    :param data: Data
    :type data: [[int, int, float, float, int, float, float, float]]
    :param key: Criteria given through the index
    :type key: int
    :return: Sorted data :type [[int, int, float, float, int, float, float, float]]
    """
    return sorted(data, key=lambda row: row[key])

def sort_by_pedestrian_id(data):
    """
    Sort data by pedestrian-id.

    :param data: Data
    :type data: [[int, int, float, float, int, float, float, float]]
    :return: Sorted data :type [[int, int, float, float, int, float, float, float]]
    """
    return sort_by(data, INDEX_TARGET_ID)

def sort_by_time_step(data):
    """
    Sort data by time-step.

    :param data: Data
    :type data: [[int, int, float, float, int, float, float, float]]
    :return: Sorted data :type [[int, int, float, float, int, float, float, float]]
    """
    return sort_by(data, INDEX_TIME_STEP)

def group_by(data, key, start, stop):
    """
    Group data by given criteria.

    :param data: Data
    :type data: [[int, int, float, float, int, float, float, float]]
    :param key: Criteria given through index
    :type key: int
    :param start: Reference value to start grouping
    :type start: int
    :param stop: Reference value to stop grouping
    :type stop: int
    :return: Grouped data :type [[[int, int, float, float, int, float, float, float]]]
    """
    result = []
    current = start
    while current <= stop:
        group =  list(filter(lambda row:row[key] == current, data))
        result.append(group)
        current = current + 1
        group = []
    return result


def group_by_time_step(data):
    """
    Group data by time-step.

    :param data: Data
    :type data: [[int, int, float, float, int, float, float, float]]
    :return: Grouped data :type [[[int, int, float, float, int, float, float, float]]]
    """
    minimum = get_minimum_time_step(data)
    maximum = get_maximum_pedestrian_id(data)
    return group_by(data, INDEX_TIME_STEP, minimum, maximum)

def group_by_pedestrian_id(data):
    """
    Group data by pedestrian_id

    :param data: Data
    :type data: [[int, int, float, float, int, float, float, float]]
    :return: Grouped data :type [[[int, int, float, float, int, float, float, float]]]
    """
    minimum = get_minimum_pedestrian_id(data)
    maximum = get_maximum_pedestrian_id(data)
    return group_by(data, INDEX_PEDESTRIAN_ID, minimum, maximum)

def select_by(data, key, val, filter):
    """
    Select data by given criteria. Select only data that meets a certain condition,
    which is specified through filter and val.

    :param data: Data
    :type data: [[int, int, float, float, int, float, float, float]]
    :param key: Criteria to select from
    :type key: int
    :param val: The value the filter has to meet
    :type val: object
    :param filter: function condition, if evaluated to true data is selected, false not
    :type filter: object
    :return: Selected data :type [[int, int, float, float, int, float, float, float]]
    """
    return [row for row in data if filter(row[key], val)]

def select_by_pedestrian_id(data, id):
    """
    Select data by pedestrian-id.

    :param data: Data
    :type data: [[int, int, float, float, int, float, float, float]]
    :param id: Pedestrian-id
    :type id: int
    :return: Selected data :type [[int, int, float, float, int, float, float, float]]
    """
    def filter(x, y):
        return x == y
    return select_by(data, INDEX_PEDESTRIAN_ID, id, filter)

def get_time_steps(data):
    """
    Get all time-steps

    :param data: Data
    :type data: [[int, int, float, float, int, float, float, float]]
    :return: List of time-steps :type [int]
    """
    return [row[INDEX_TIME_STEP] for row in data]

def get_minimum_time_step(data):
    """
    Get minimum time-step
    :param data: Data
    :type [[int, int, float, float, int, float, float, float]]
    :return: Minimum time-step :type int
    """
    return min(get_time_steps(data))

def get_maximum_time_step(data):
    """
    Get maximum time-step
    :param data: Data
    :type [[int, int, float, float, int, float, float, float]]
    :return: Maximum time-step :type int
    """
    return max(get_time_steps(data))

def get_pedestrian_ids(data):
    """
    Get all pedestrian-ids

    :param data: Data
    :type data: [[int, int, float, float, int, float, float, float]]
    :return: Pedestrian-ids :type [int]
    """
    return [row[INDEX_PEDESTRIAN_ID] for row in data]

def get_minimum_pedestrian_id(data):
    """
    Get minimum pedestrian-id

    :param pedestrian_ids: List of pedestrian-ids
    :type pedestrian_ids: [int]
    :return: Minimum pedestrian-id :type int
    """
    return min(get_pedestrian_ids(data))

def get_maximum_pedestrian_id(data):
    """
    Get maximum pedestrian-id

    :param pedestrian_ids: List of pedestrian-ids
    :type pedestrian_ids: [int]
    :return: Maximum pedestrian-id :type int
    """
    return max(get_pedestrian_ids(data))

# extracts the observation area of the camera from the data
def extract_observation_area(data, area):
    x = area[0]
    y = area[1]
    width = area[2]
    height = area[3]
    return ([row for row in data if (x <= row[INDEX_POSITION_X] <= (x + width)) and
             (y <= row[INDEX_POSITION_Y] <= (y + height))])

# reduces data
# takes only every "framerate" timestep
def extract_framerate(data, framerate):
    data_reduced = []
    for time in data:
        if time[0][0] % framerate == 0:
            data_reduced.append(time)

    return data_reduced

# # sorts the data chronologicaly by timestep
# # new format: [[list of all data for timestep 1], [list of all data for timestep 2], [...], ... ]
# def sort_chronological(data):
#     #print("length: ",len(data))
#     data_sorted = sorted(data, key=lambda row:row[INDEX_TIME_STEP])
#     current_time = data_sorted[0][INDEX_TIME_STEP]
#     data_chron = []
#     rows_equal_time = []
#     chron_len = 0
#     for row in data_sorted:
#         if row[INDEX_TIME_STEP] == current_time:
#             rows_equal_time.append(row)
#         else:
#             data_chron.append(rows_equal_time)
#             chron_len = chron_len + len(rows_equal_time)
#             rows_equal_time = []
#             rows_equal_time.append(row)
#             current_time += 1
#
#     return data_chron

# Helper method for mapping non 100% distributions to the correct scale
def map_to_100_percent(dist):
    dist = np.round(dist,2)
    factor = 1 / np.sum(dist)
    dist = np.round([dist[0] * factor, dist[1] * factor, dist[2] * factor],2)
    return dist




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

