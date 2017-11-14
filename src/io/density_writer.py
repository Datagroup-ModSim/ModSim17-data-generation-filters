import numpy as np


def write_matrix_to_file(matrix, dist, file):
    number_of_elements = np.size(matrix)
    row = np.reshape(matrix, (1, number_of_elements)).flatten()
    row = np.concatenate((row, dist))
    row_string = ';'.join(map(str,row)) + '\n'
    file.write(row_string)
    file.flush()


def write_to_csv(timeseries, path, file_name, dist):
    i_max = len(timeseries) - 1

    with open(path+file_name,mode='a') as file:

        for i in range(0, i_max):

            number_of_elements = np.size(timeseries[i])
            row = np.reshape(timeseries[i], (1,number_of_elements)).flatten()
            row = np.concatenate((row,dist))

            file.write(row)


def get_output_file_name(dist, name='density_'):
    return name + str(int(dist[0]*100)) + '_' + str(int(dist[1]*100)) + '_' + str(int(dist[2]*100))

