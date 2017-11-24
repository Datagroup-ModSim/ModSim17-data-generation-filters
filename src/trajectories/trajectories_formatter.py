import numpy as np

INDEX_TIME_STEP = 0
INDEX_PED_ID = 1
INDEX_POS_X = 2
INDEX_POS_Y = 3
INDEX_TARGET_ID = 4


def format_trajectories(data, file):
    data_v = np.vstack(data)
    data_v = sorted(data_v, key=lambda row:row[INDEX_PED_ID])
    current_id = data_v[0][INDEX_PED_ID]
    data_sorted_id = []
    ped_data = []
    # format array by id
    for row in data_v:
        if row[INDEX_PED_ID] == current_id:
            ped_data.append(row)
        else:
            data_sorted_id.append(ped_data)
            current_id = row[INDEX_PED_ID]
            ped_data = []
            ped_data.append(row)

    velocity = []
    for ped in data_sorted_id:
        pos_start = [ped[0][INDEX_POS_X], ped[0][INDEX_POS_Y]]
        pos_end = [ped[-1][INDEX_POS_X], ped[-1][INDEX_POS_Y]]
        time_delta = ped[-1][INDEX_TIME_STEP] - ped[0][INDEX_TIME_STEP]
        v_y = (pos_end[1]-pos_start[1])
        v_y = v_y/time_delta
        velocity.append([v_y,ped[0][INDEX_PED_ID]])

    max_velocity = sorted(velocity, key=lambda row:row[0]) # sort velocities
    fastest_ped_id = max_velocity[-1][1]


    # write to file
    file.write_to_file()


def norm_trajectories(data):
    data_normed = []
    return data_normed

