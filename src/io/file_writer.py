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


def get_output_file_name(distribution, name='_density'):
    return str(int(distribution[0])) + '-' + str(int(distribution[1])) + '-' + str(int(distribution[2])) + name


header = "# This file contains all information regarding the generated output data"
section_header = ["# Datatype", "# script version tag","SCENARIO SIZE","# OBSERVATION AREA",
                  "# TIME STEP_BOUNDS", "# RESOLUTION ", "# SIGMA", "# GAUSS_DENSITY BOUNDS","# FRAMERATE" ,"# scenarios used"]


def generate_attributes_file(out_dir, section_fields):
    with open(out_dir+"\\"+"attributes.txt", mode='w', newline='\n') as file:
        file.writelines(header)
        file.writelines('\n')
        file.writelines('\n')
        for i in range(0, len(section_fields)):
            file.writelines(section_header[i])
            file.writelines('\n')
            file.writelines(section_fields[i])
            file.writelines('\n')
            file.writelines('\n')

        file.flush()

