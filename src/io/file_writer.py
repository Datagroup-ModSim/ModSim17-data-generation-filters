import numpy as np
import os


def create_output_directory(input_directory, output_directory):
    folders = input_directory.split('/')[1:-2]
    output_directory = output_directory + '/' + '/'.join(folders)
    if not os.path.exists(output_directory):
        print('FileWriter: create ' + output_directory)
        os.makedirs(output_directory)
    return output_directory


def write_density_timeseries(timeseries, path, total_distribution, momentary_distribution, unique_id):
    file_name = get_output_file_name(total_distribution)
    path = path + '/' + file_name + str(unique_id) + '.csv'
    print('FileWriter: write to ' + path)
    file = open(path, mode='a')
    i_max = len(timeseries)
    for i in range(0,i_max):
        number_of_elements = np.size(timeseries[i])
        row = np.reshape(timeseries[i], (1, number_of_elements)).flatten()
        row = np.concatenate((row, momentary_distribution[i]))
        row_string = ';'.join(map(str, row)) + '\n'
        file.write(row_string)
    file.close()
    unique_id = unique_id + 1
    return unique_id


def write_trajectories_formatted(trajectory_formatted, current_output_directory, unique_id):
    file_name = "trajectories_"
    path = current_output_directory +'/' +file_name + str(unique_id+1) + ".csv"

    with open(path, mode='a') as file:
        for row in trajectory_formatted:
            row_string = ';'.join(map(str, row)) + '\n'
            file.writelines(row_string)
            file.flush()

    unique_id+=1

    return unique_id


def get_output_file_name(distribution, name='_density'):
    return str(int(distribution[0])) + '-' + str(int(distribution[1])) + '-' + str(int(distribution[2])) + name


# TODO Test
header = "# This file contains all information regarding the generated output data"
sections_density = ["# RESOLUTION ", "# SIGMA", "# GAUSS_DENSITY BOUNDS","# FRAMERATE"]
end_section = "# data files used"

def generate_attributes_file_density(files_used,observation_area, output_path, scenario_size, density_constants):

    with open(output_path+"\\"+"attributes.txt", mode='w', newline='\n') as file:
        file.writelines(header)
        file.writelines('\n')
        file.writelines("# datatype" + '\n' + "trajectories")
        file.writelines("# version number" + '\n' + "1.0")
        file.writelines("# sencario size" + '\n' + scenario_size)
        file.writelines("# observation area" + '\n' + str(observation_area))

        for n in range(0, len(sections_density)):
            file.writelines(sections_density[n])
            file.writelines(str(density_constants[n]))

        file.writelines(end_section)
        file.writelines(files_used)
        file.flush()


def generate_attributes_file_trajectories(files_used, observation_area, output_path, scenario_size):

    with open(output_path+"\\"+"attributes.txt", mode='w', newline='\n') as file:
        file.writelines(header)
        file.writelines('\n')
        file.writelines("# datatype" + '\n' + "trajectories")
        file.writelines("# version number" + '\n' + "1.0")
        file.writelines("# sencario size" + '\n' + scenario_size)
        file.writelines("# observation area" + '\n' + str(observation_area))

        file.writelines(end_section)
        file.writelines(files_used)
        file.flush()


