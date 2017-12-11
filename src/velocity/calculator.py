import math

from src.util.helper import get_maximum_pedestrian_id, get_pedestrian_ids, select_by_pedestrian_id

INDEX_TIME_STEP = 0
INDEX_PEDESTRIAN_ID = 1
INDEX_POSITION_X = 2
INDEX_POSITION_Y = 3
INDEX_TARGET_ID = 4
INDEX_VELOCITY_ABSOULTE = 5
INDEX_VELOCITY_X = 6
INDEX_VELOCITY_Y = 7

def calculate_velocity_vectors(data):
    """
    Calculate velocity vectors from absolute velocity and step length.
    Append velocity_x and velocity_y to each row. Pedestrians are
    processed sequentially by their id.

    :param data: Snapshots of pedestrian movement
    :type data: [int, int, float, float, int, float]
    :return: Input data and appended velocity_x and velocity_y :type [int, int, float, float, int, float, float, float]
    """
    maximum_pedestrian_id = get_maximum_pedestrian_id(data)
    result = []
    for id in range(1, maximum_pedestrian_id + 1):
        selected = select_by_pedestrian_id(data, id)
        result.extend(calculate_velocity_vector(selected))
    return result

def calculate_velocity_vector(pedestrian_snapshots):
    """
    Helper to calculate velocity vectors for one pedestrian over a period.

    :param pedestrian_snapshots: Messured positions and absolute velocities
    :type pedestrian_snapshots: [int, int, float, float, int, float]
    :return: velocity in x and y direction and input data :type [int, int, float, float, int, float, float, float]
    """
    if not pedestrian_snapshots:
        return []
    else:
        result = []
        first_row = pedestrian_snapshots[0]
        first_row.extend([0.0, 0.0])
        result.append(first_row)
        for i in range(1, len(pedestrian_snapshots)):
            previous = pedestrian_snapshots[i - 1]
            current = pedestrian_snapshots[i]
            if current[INDEX_VELOCITY_ABSOULTE] == 0:
                row = current
                row.extend([0.0, 0.0])
                result.append(row)
            else:
                prev_pos_x = previous[INDEX_POSITION_X]
                prev_pos_y = previous[INDEX_POSITION_Y]
                cur_pos_x = current[INDEX_POSITION_X]
                cur_pos_y = current[INDEX_POSITION_Y]
                diff_x = cur_pos_x - prev_pos_x
                diff_y = cur_pos_y - prev_pos_y
                vel_abs = current[INDEX_VELOCITY_ABSOULTE]
                to_unit_length = 1 / math.sqrt(diff_x**2 + diff_y**2)
                vel_x = diff_x * to_unit_length * vel_abs
                vel_y = diff_y * to_unit_length * vel_abs
                row = current
                row.extend([vel_x, vel_y])
                result.append(row)
        return result