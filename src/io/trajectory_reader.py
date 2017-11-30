import csv

from glob import glob
from src.velocity.calculator import calculate_velocity_vectors


def get_input_file_names(path, file_names):
    """
    Search for all input files in a given directory.
    Specifing multiple file names is possible.

    :param path: Path to input-file-directory
    :type path: str
    :param file_names: File names to search for
    :type file_names: [str]
    :return: List of relative path to input file locations
    """
    input_file_names = []
    for i in range(0, len(file_names)):
        input_file_names.extend(glob(path + '/' + file_names[i]))
    return input_file_names

def read_trajectories(trajectories_file_name):
    """
    Read one .trajectories file and convert its content to numerical data

    :param trajectories_file_name: relative path to .trajectories file
    :type trajectories_file_name: str
    :return: Two dimensional list of trajectories-data. One row consists of the following
             time_step, pedestrian_id, pos_x, pos_y, target_id
    """
    result = []
    print(trajectories_file_name)
    #field_names = ['timeStep', 'pedestrianId', 'x', 'y', 'targetId']
    file = open(trajectories_file_name, newline='')
    csv.register_dialect('trajectories', delimiter=' ')
    trajectories_file = csv.DictReader(file, dialect='trajectories')
    for row in trajectories_file:
        time_step = int(row['timeStep'])
        pedestrian_id = int(row['pedestrianId'])
        pos_x = float(row['x'])
        pos_y = float(row['y'])
        target_id = int(row['targetId'])
        result_row = [time_step, pedestrian_id, pos_x, pos_y, target_id]
        result.append(result_row)
    return result

def read_velocity(velocity_file_name):
    """
    Read one "output_ts_pid.txt" file, which holds pedestrian input values.
    Convert input to numeric values.

    :param velocity_file_name: Relative path to a output_ts_pid.txt file
    :type velocity_file_name: str
    :return: List of velocities
    """
    result = []
    #field_names = ['input']
    file= open(velocity_file_name, newline='\n')
    csv.register_dialect('velocity', delimiter=';')
    velocity_file = csv.DictReader(file, dialect='velocity')
    for row in velocity_file:
        velocity = float(row['velocity'])
        result.append(velocity)
    return result

def merge_trajectories_and_velocities(trajectories, velocities):
    """
    Merge each trajectory with its corresponding velocity.

    :param trajectories: Trajectory data
    :type trajectories: [int, int, float, float, int]
    :param velocities: Velocity data
    :type velocities: [float]
    :return: Combined trajectories and velocities
    """
    result = []
    if len(trajectories) == len(velocities):
        for i in range(0, len(trajectories)):
            row = trajectories[i]
            row.extend([velocities[i]])
            result.append(row)
        return result
    else:
        print('Error: unequal number of trajectories and velocities')
        return None

def get_data(path, file_names):
    """
    Execute all neccessary operations to get input data (trajectories and velocities).

    :param path: Relative path to input file directory.
    :type path: str
    :param file_names:  File names to search for, globbing is enabled
    :return: Trajectory and input data
    """
    input_file_names = get_input_file_names(path, file_names)
    data_trajectories = read_trajectories(input_file_names[0])
    data_velocity = read_velocity(input_file_names[1])
    data = merge_trajectories_and_velocities(data_trajectories, data_velocity)
    data = calculate_velocity_vectors(data)
    return data