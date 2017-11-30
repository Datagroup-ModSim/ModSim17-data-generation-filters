# filter methods for density Data list
# thresholding
#
#

import numpy as np

def filter_data(density_timeseries):
    normalizeDensities(density_timeseries)
    for matrix in density_timeseries:
        matrix = matrix/maxVal
    density_timeseries = thresholding(density_timeseries, 0.5)

    return density_timeseries

def thresholding(density_timeseries, threshold):
    for matrix in density_timeseries:
        for x in np.nditer(matrix):
            if x >= threshold:
                x = 1
            else:
                x = 0
    return density_timeseries




def normalizeDensities(density_timeseries):
    maxValuesList = []
    for matrix in density_timeseries:
        maxValuesList.append(matrix.max())
    maxVal = max(maxValuesList)

    for matrix in density_timeseries:
        matrix = matrix/maxVal
    

