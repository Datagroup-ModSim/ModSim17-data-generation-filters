import numpy as np


def write_to_csv(timeseries, path, file_name, count):
    i_max = len(timeseries) - 1
    for i in range(0, i_max):
        destination = path + '/' + str(count) + '_' + file_name + '_' + str(i) + '.csv'
        #print(destination)
        print(np.array_equal(timeseries[0], timeseries[i]))
        np.savetxt(destination, timeseries[i], delimiter=';', fmt='%1.4f') # TODO


def write_to_csv(timeseries, path, file_name, dist):
    i_max = len(timeseries) - 1

    with open(path+file_name,mode='a') as file:

        for i in range(0, i_max):

            #test_density_data(timeseries[i],path,file_name + str(count), resize=False) # Test Bilder
            number_of_elements = np.size(timeseries[i])
            row = np.reshape(timeseries[i], (1,number_of_elements)).flatten()
            row = np.concatenate((row,dist))

            file.write(row)

def write_matrix_to_file(matrix, path, file_name, timestep, count):
    destination = path + '/' + file_name + '_' + str(count) + str(timestep) + '.csv'
    np.savetxt(destination, matrix, delimiter=';', fmt='%1.4f')


def get_output_file_name(dist, name='density_'):
    return name + str(int(dist[0]*100)) + '_' + str(int(dist[1]*100)) + '_' + str(int(dist[2]*100))

