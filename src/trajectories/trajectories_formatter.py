import numpy as np


INDEX_TIME_STEP = 0
INDEX_PED_ID = 1
INDEX_POS_X = 2
INDEX_POS_Y = 3
INDEX_TARGET_ID = 4


def sort_by_id(data):
    data = np.vstack(data)
    data = sorted(data, key=lambda row: [row[INDEX_PED_ID],row[INDEX_TIME_STEP]]) # sort by id and then by time
    current_id = data[0][INDEX_PED_ID]
    data_sorted_id = []
    ped_data = []
    # format array by id
    for row in data:
        if row[INDEX_PED_ID] == current_id:
            ped_data.append(row)
        else:
            data_sorted_id.append(ped_data)
            current_id = row[INDEX_PED_ID]
            ped_data = []
            ped_data.append(row)

    return data_sorted_id


def remove_duplicate_steps(ped):
    i = 0
    while i < len(ped):
        cur_step = ped[i]
        cur_xy = cur_step[INDEX_POS_X:INDEX_POS_Y + 1]
        duplicate_indexes = []
        for j in range(i+1,len(ped)):
            cmp_xy = ped[j][INDEX_POS_X:INDEX_POS_Y+1]
            if np.array_equal(cur_xy,cmp_xy):
                duplicate_indexes.append(j)

        duplicate_indexes = sorted(duplicate_indexes, reverse=True)
        for index in duplicate_indexes:
            del ped[index]
        i += 1


def remove_duplicates(data):
    for ped in data:
        remove_duplicate_steps(ped)

    return data


def find_fastest_ped(data):
    ped_information = []
    for ped in data:
        if len(ped) > 1:
            step_size = get_largest_step(ped)
            ped_information.append([2-step_size,len(ped),step_size, ped[0][INDEX_PED_ID]])

    # sort velocities by len of ped and then by velocity
    # ped_information_sorted = sorted(ped_information, key=lambda row: row[0]) # by step size
    test_sort_length = sorted(ped_information, key=lambda row: row[1]) # by length
    return test_sort_length[0]


#   Normalize the trajectories by applying intervals on the y-axis and always taking one step per intervall.
#   This is only done if the pedestrian has more steps than the norm pedestrian.
#
#   :param data: Trajectory data sorted by id
#   :type trajectories: [int, int, float, float, int]
#   :param norm_ped_info: information of the norm pedestrian [velocity,number_of_steps,id]
#   :type norm_ped_info: [float,float,float]
#   :return: norm_data: type [[int, int, float,float, int]]
def norm_ped_data(data, norm_ped_info, area):
    step_size = norm_ped_info[2]
    height = area[3]
    number_intervals = int(height / step_size)

    norm_data = []
    number_of_peds_lost = 0
    for ped in data:
        if len(ped) > number_intervals:
            new_ped = apply_interval(ped, step_size, number_intervals, area)
            if len(new_ped) == number_intervals:
                norm_data.append(new_ped)
            else:
                number_of_peds_lost+=1
        elif len(ped) == number_intervals:
            norm_data.append(ped)
        else:
            print("smaller length -> should not be!!!")
    print("number of pedestrians deleted: ", number_of_peds_lost)
    return norm_data


def get_largest_step(norm_ped):
    step_size = -1
    for i in range(0, len(norm_ped) - 1):
        cur_step_size = np.subtract(norm_ped[i + 1][INDEX_POS_Y], norm_ped[i][INDEX_POS_Y])
        if cur_step_size > step_size:
            step_size = cur_step_size
    return step_size


def apply_interval(ped, step_size,number_intervals, area):
    height = area[3]
    y_min = area[1]
    y_max = area[1] + height

    new_ped = []
    for k in range(0, number_intervals - 1):
        lower_bound = y_min + k * step_size
        upper_bound = lower_bound + step_size
        step_new = get_step(ped, lower_bound, upper_bound)
        if np.all(step_new) != None:
            new_ped.append(step_new)

    # end interval from last upper_bound until y_max, incase height dose not evenly divide by step_size
    lower_bound = y_min + (number_intervals-1) * step_size
    upper_bound = y_max
    step_new = get_step(ped, lower_bound, upper_bound)
    if np.all(step_new) != None:
        new_ped.append(step_new)
    return new_ped


def get_step(ped, lower_bound, upper_bound):
    steps_inside_interval = [step for step in ped if lower_bound <= step[INDEX_POS_Y] < upper_bound]
    if len(steps_inside_interval) > 0:
        return steps_inside_interval[0]
    else:
        return None


def format_norm_data(norm_data):

    data_formatted = []
    for ped in norm_data:
        steps = [step[INDEX_POS_X:INDEX_POS_Y+1] for step in ped]
        steps = list(np.ravel(steps))
        steps = list(np.round(steps,4))
        target_id = remap_targets(ped[0][INDEX_TARGET_ID])
        steps.append(target_id)
        data_formatted.append(steps)

    return data_formatted


def remap_targets(target_id):
    if int(target_id) == 4:
        return 0
    elif int(target_id) == 5:
        return 1
    elif int(target_id) == 6:
        return 2


def format_trajectories(data, area):
    # sort data by id
    data_sorted_id = sort_by_id(data)
    # remove duplicate steps
    data_no_duplicates = remove_duplicates(data_sorted_id)
    # find the ped that has the fewest steps and is fastest
    norm_ped_info = find_fastest_ped(data_no_duplicates)
    # norm the data by the fastest
    norm_data = norm_ped_data(data_no_duplicates, norm_ped_info, area)

    # test lengths
    lengths = []
    for ped in norm_data:
        lengths.append(len(ped))


    print("length of steps", set(lengths))
    if len(list(set(lengths))) != 1:
        print("error -------------------------------------------------------")

    print("\n")

    # bring data in form
    # ped1: [x,y,x,y,x,y,...,targetid]
    # ped2: [x,y,x,y,x,y,...,targetid]
    format_data = format_norm_data(norm_data)

    return format_data
