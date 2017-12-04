# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 16:31:27 2017

@author: Anita
"""

import numpy as np
import numpy.linalg as lin

#from src.tests.density_plot_tests import plot_density

def mainPCA(density_timeseries):
    
    #orginal = density_timeseries.copy()
    #mse = [None] * len(density_timeseries)
    for i in range(0, len(density_timeseries)):
        density_timeseries[i] = singlePCA(density_timeseries[i])
        #density_timeseries[i], mse[i] = singlePCA(density_timeseries[i])

    return density_timeseries


def singlePCA(matrix):
    svCut = 0.1
    
    U, s, V = lin.svd(matrix)
    
    rlen, clen = matrix.shape
    S = np.zeros((rlen, clen), dtype=complex)
    S[:min(rlen, clen), :min(rlen, clen)] = np.diag(s)
    
    modes = sum(x > svCut for x in s)
    matrixReduced = np.dot(U[:, :modes], np.dot(S[:modes,:modes], V[:modes,:])).real.clip(min=0)
    
    #mse = ((matrix - matrixReduced) ** 2).mean(axis=None)    
    #print(np.allclose(matrix, matrixReduced, rtol=1e2, atol=1e-3), modes)
    # plot_density(reduced, "testSVD****", "reduced")
    # plot_density(matrix, "testSVD****", "orginal")
    return matrixReduced #, mse
