import numpy as np

def write_to_csv(timeseries, path, file_name, count):
    i_max = len(timeseries) - 1
    for i in range(0, i_max):
        destination = path + '/' + str(count) + '_' + file_name + '_' + str(i) + '.csv'
        print(destination)
        np.savetxt(destination, timeseries[0], delimiter=';', fmt='%1.4f')

def get_output_file_name(dist):
    return 'density_' + str(int(dist[0]*100)) + '_' + str(int(dist[1]*100)) + '_' + str(int(dist[2]*100))
