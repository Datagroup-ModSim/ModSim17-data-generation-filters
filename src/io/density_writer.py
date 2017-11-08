import numpy as np


def write_to_csv(timeseries, path, file_name, count):
    i_max = len(timeseries) - 1
    for i in range(0, i_max):
        destination = path + '/' + str(count) + '_' + file_name + '_' + str(i) + '.csv'
        #print(destination)
        np.savetxt(destination, timeseries[0], delimiter=';', fmt='%1.4f') # TODO


def write_matrix_to_file(matrix, path, file_name, timestep, count):
    destination = path + '/' + file_name + '_' + str(count) + '_dist_' + str(timestep)
    np.savetxt(destination, matrix, delimiter=';', fmt='%1.4f')


def get_output_file_name(dist, name='density_'):
    return name + str(int(dist[0]*100)) + '_' + str(int(dist[1]*100)) + '_' + str(int(dist[2]*100))

