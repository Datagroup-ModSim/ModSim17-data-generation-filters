
# extracts the observation area of the camera from the data
def extract_observation_area(data, area):
    x = area[0]
    y = area[1]
    width = area[2]
    height = area[3]
    return ([row for row in data if (x <= row[INDEX_POS_X] <= (x + width)) and
             (y <= row[INDEX_POS_Y] <= (y + height))])

# reduces data
# takes only every "framerate" timestep
def extract_framerate(data, framerate):
    data_reduced = []
    for time in data:
        if time[0][0] % framerate == 0:
            data_reduced.append(time)

    return data_reduced

# sorts the data chronologicaly by timestep
# new format: [[list of all data for timestep 1], [list of all data for timestep 2], [...], ... ]
def sort_chronological(data):
    #print("length: ",len(data))
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

