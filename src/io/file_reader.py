import csv

from glob import glob
from src.velocity.calculator import calculate_velocity_vectors
from src.util.helper import extract_observation_area, extract_framerate, extract_recording_period


class FileReader:

    def __init__(self, input_directory, glob_pattern):
        self.index = 0
        self.input_file_names = get_input_file_names(input_directory, glob_pattern)
        self.is_finished = False

    def increment_index(self):
        if self.index < len(self.input_file_names) - 1:
            self.index = self.index + 1
        else:
            print('FileReader: All inputs are read.')
            self.is_finished = True

    def get_next_data(self, observation_area, frame_rate, recording_percentage, calculate_velocity):
        file_names = self.input_file_names[self.index]
        # read from all neccessary input files
        data_trajectories = read_trajectories(file_names)

        # if selected calulcate velocitys and merge the data
        if calculate_velocity:
            data_velocity = read_velocity(file_names[1])
            # calculate vectorial velocities
            data_velocity = calculate_velocity_vectors(data_velocity)
            # merge trajectories and absolute velocities
            data = merge_trajectories_and_velocities(data_trajectories, data_velocity)

        else:
            data = data_trajectories

        # select camera observation area
        data = extract_observation_area(data, observation_area)
        # select not every snapshot to enhance performance
        data = extract_framerate(data, frame_rate)
        # select snapshots filled with pedestrians
        data = extract_recording_period(data, recording_percentage)
        # flatten data
        data = [row for time_steps in data for row in time_steps]

        folders = file_names[0].split('/')[:-1]
        current_folder = '/'.join(folders)
        print('FileReader: read from ' + current_folder)

        self.increment_index()

        return data, file_names[0]


def get_input_file_names(path, glob_pattern):
    """
    Search for all input files in a given directory.
    Specifing multiple file names is possible.

    :param path: Path to input-file-directory
    :type path: str
    :param glob_pattern: File names to search for
    :type glob_pattern: [str]
    :return: List of relative path to input file locations :type [str]
    """
    trajectories_files = glob(path + '/' + glob_pattern[0], recursive=True)
    #velocity_files = glob(path + '/' + glob_pattern[1], recursive=True)
    return trajectories_files#list(zip(trajectories_files, velocity_files))


def read_trajectories(trajectories_file_name):
    """
    Read one .trajectories file and convert its content to numerical data

    :param trajectories_file_name: relative path to .trajectories file
    :type trajectories_file_name: str
    :return: Two dimensional list of trajectories-data. One row consists of the following
             time_step, pedestrian_id, pos_x, pos_y, target_id
    """
    result = []
    # field_names = ['timeStep', 'pedestrianId', 'x', 'y', 'targetId']
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
    file.close()
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
    # field_names = ['input']
    file = open(velocity_file_name, newline='\n')
    csv.register_dialect('velocity', delimiter=';')
    velocity_file = csv.DictReader(file, dialect='velocity')
    for row in velocity_file:
        velocity = float(row['velocity'])
        result.append(velocity)
    file.close()
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
