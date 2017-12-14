# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 16:31:27 2017

@author: Anita
"""

import numpy as np
import numpy.linalg as lin

from src.filter.density_plot_tests import plot_density

def mainPCA(density_timeseries, keepPercentage=99, centerMatrix=False, meanMatrix=False):
# =============================================================================
# Durchführen einer Hauptkomponentenanalyse
# Übergabewerte:
# density_timeseries: Liste aus Matrizen der Dichtedaten
# keepPercetage: Prozentualer Anteil an Informationen der behalten werden soll
# centerMatrix: Bei True wird die Matrix vor der Zerlegung Zentriert
# meanMatrix: Bei True wird der Mittelwert von allen Matrizen aus
#             density_timeseries berechnet und von jeder Matix subrahiert
# Ausgabewerte:
# PCA: Aus U^T, s, V^T zusammengesetzte Matrix
# Optional können auch die Listen aller U (linke Singulärvektoren), 
# s (Singulärwerte) und V(rechte Singulärvektoren) ausgegeben werden
# =============================================================================

    # Liste für Matrizen mit linken Singulärvektoren
    U = [None] * len(density_timeseries)
    # Liste für Vektoren mit Singulärwerten
    s = [None] * len(density_timeseries)
    # Liste für Matrizen mit rechten
    V = [None] * len(density_timeseries)
    PCA = [None] * len(density_timeseries)

    # Berechnen der durchschnittlichen Matrix aller Zeitschritte falls gewünscht
    if meanMatrix:
        meanMatrix = calculate_Mean_Matrix(density_timeseries)    

    # Berechnen der PCA aller Matrizen
    for i in range(0, len(density_timeseries)):
        matrix = density_timeseries[i]
        if meanMatrix:
            matrix = matrix - meanMatrix
        U[i], s[i], V[i] = singlePCA(matrix, keepPercentage, centerMatrix)
        PCA[i] = np.concatenate((np.transpose(U[i]), s[i], V[i]), axis=1)

    return PCA
    # return U, s, V
    


def singlePCA(matrix, keepPercentage=99, centerMatrix=False):
    # Berechnen der PCA für eine Matrix bei der keepPercentage der 
    # Originalinformation behalten werden und die Matrix optional
    # vor der Zerlegung zentriert wird.

    # Matrix zentrieren
    if centerMatrix is True:
        colMeans = np.mean(matrix, axis=0)
        matrix = matrix - colMeans

    # Singulärwertzerlegung
    U, s, V = lin.svd(matrix)

    # Berechnen der zu behaltenden Singulärwerte um keepPercentage des Bildes zu behalten
    percentage = np.cumsum(s) / sum(s) * 100
    modes = sum(percentage < keepPercentage) + 1

    # Abschneiden der reduzierten Matrizen
    U = U[:, :modes]
    s = s[:modes]
    V = V[:modes, :]

    return U, s, V 


def calculate_Mean_Matrix(density_timeseries):

    meanMatrix = np.mean(density_timeseries, axis=0)
    return meanMatrix


##################################Tests########################################
def mainPCAtest(density_timeseries, mean, central):

    # orginal = density_timeseries.copy()
    mse = [None] * len(density_timeseries) * 5
    modes = [None] * len(density_timeseries) * 5
    
    if mean is True:
        meanMatrix = calculate_Mean_Matrix(density_timeseries)

    index = 0
    for i in range(0, len(density_timeseries)):
        if i % 50 == 0:
            picture = True
        else:
            picture = False
        for per in [99, 95, 90, 75, 50]:
            matrix = density_timeseries[i]
            if mean is True:
                matrix = matrix - meanMatrix
            mse[index], modes[index] = testPCA(matrix, per, picture, i, central)
            if picture is True:
                plot_density(density_timeseries[i], (str(i) + "_****"), "Orginal")
            index += 1

    return mse, modes


def testPCA(matrix, keepPercentage, picture, i, centerMatrix):

    # Matrix zentrieren
    if centerMatrix is True:
        colMeans = np.mean(matrix, axis=0)
        matrix = matrix - colMeans

    # Singulärwertzerlegung
    U, s, V = lin.svd(matrix)

    # Singulärwertevektor als Diagonalelemente in Matrix einsetzen
    rlen, clen = matrix.shape
    S = np.zeros((rlen, clen), dtype=complex)
    S[:min(rlen, clen), :min(rlen, clen)] = np.diag(s)

    # Berechnen der zu behaltenden Singulärwerte um keepPercentage des Bildes zu behalten
    percentage = np.cumsum(s) / sum(s) * 100
    modes = sum(percentage < keepPercentage) + 1

    # Wieder zusammensetzten der Matrix mit weniger Singulärwerten
    matrixReduced = np.dot(U[:, :modes], np.dot(S[:modes,:modes], V[:modes,:])).real # .clip(min=0)

    mse = ((matrix - matrixReduced) ** 2).mean(axis=None)
    # print(np.allclose(matrix, matrixReduced, rtol=1e2, atol=1e-3), modes)
    if picture is True:
        if(np.min(matrixReduced) < 0):
            matrixReduced = matrixReduced - np.min(matrixReduced)
        plot_density(matrixReduced, (str(i) + "_PCAreduced****"), ("_" + str(keepPercentage)))
    # plot_density(matrix, "****", "orginal")
    return mse, modes
