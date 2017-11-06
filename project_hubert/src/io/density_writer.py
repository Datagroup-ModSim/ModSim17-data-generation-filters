import numpy as np

def write_to_csv(path, timeseries, dist):
    print(len(timeseries))
    for i in range(0, 10000):
        #print(path + '/density_gauss' + str(i) + '_' + str(int(dist[0]*100)) + '_' + str(int(dist[1]*100)) + '_' + str(int(dist[2]*100)) + '.csv')
        np.savetxt(path + '/density_gauss' + str(i) + '_' + str(int(dist[0]*100)) + '_' + str(int(dist[1]*100)) + '_' + str(int(dist[2]*100)) + '.csv', timeseries[i], delimiter=';', fmt='%1.4f')
