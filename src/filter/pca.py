# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 16:31:27 2017

@author: Anita
"""

import numpy as np
import numpy.linalg as lin

from src.filter.density_plot_tests import plot_density

def mainPCA(density_timeseries):

    for i in range(0, len(density_timeseries)):
        density_timeseries[i] = singlePCA(density_timeseries[i])

    return density_timeseries


def singlePCA(matrix, keepPercentage=90):

    # Matrix zentrieren
    # colMeans = np.mean(matrix, axis=0)
    # matrix = matrix - colMeans

    # Singulärwertzerlegung
    U, s, V = lin.svd(matrix)

    # Singulärwertevektor als Diagonalelemente in Matrix einsetzen
    rlen, clen = matrix.shape
    S = np.zeros((rlen, clen), dtype=complex)
    S[:min(rlen, clen), :min(rlen, clen)] = np.diag(s)

    # Berechnen der zu behaltenden Singulärwerte um keepPercentage des Bildes zu behalten
    percentage = np.cumsum(s)/sum(s)*100    
    modes = sum(percentage < keepPercentage)

    # Wieder zusammensetzten der Matrix mit weniger Singulärwerten
    matrixReduced = np.dot(U[:, :modes], np.dot(S[:modes,:modes], V[:modes,:])).real # .clip(min=0)

    return matrixReduced


def mainPCAtest(density_timeseries):

    #orginal = density_timeseries.copy()
    mse = [None] * len(density_timeseries) * 5
    modes = [None] * len(density_timeseries) * 5

    index = 0
    for i in range(0, len(density_timeseries)):
        if i % 50 == 0:
            picture = True
        else:
            picture = False
        for per in [99, 95, 90, 75, 50]:
            mse[index], modes[index] = testPCA(density_timeseries[i], per, picture, i)
            if picture == True:
                plot_density(density_timeseries[i], "Orginal****", i)
            index += 1

    return density_timeseries


def testPCA(matrix, keepPercentage, picture, i):

    # colMeans = np.mean(matrix, axis=0)
    # matrix = matrix - colMeans
    
    U, s, V = lin.svd(matrix)
    
    rlen, clen = matrix.shape
    S = np.zeros((rlen, clen), dtype=complex)
    S[:min(rlen, clen), :min(rlen, clen)] = np.diag(s)
    
    percentage = np.cumsum(s)/sum(s)*100    
    modes = sum(percentage < keepPercentage)
    matrixReduced = np.dot(U[:, :modes], np.dot(S[:modes,:modes], V[:modes,:])).real # .clip(min=0)
    
    mse = ((matrix - matrixReduced) ** 2).mean(axis=None)    
    #print(np.allclose(matrix, matrixReduced, rtol=1e2, atol=1e-3), modes)
    if picture == True:
        if(np.min(matrixReduced) < 0):
            matrixReduced = matrixReduced - np.min(matrixReduced)
        describePicture = str(i) + "_" + str(keepPercentage) + str(modes) + str(np.max(mse))
        plot_density(matrixReduced, "PCAreduced****", describePicture)
    #plot_density(matrix, "****", "orginal")
    return mse, modes
