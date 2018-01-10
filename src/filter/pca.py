# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 16:31:27 2017

@author: Anita
"""

import numpy as np
import numpy.linalg as lin

from src.filter.density_plot_tests import plot_density

def mainPCA(density_timeseries, keepPercentage=99, keepModes=0, substractTimesteps=False, \
            addTimesteps=0, addMultibleTimesteps=0, centerMatrix=False, \
            meanMatrix=False, recombine=False):
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

    length = len(density_timeseries)
    # Liste für Matrizen mit linken Singulärvektoren
    U = [None] * length
    # Liste für Vektoren mit Singulärwerten
    s = [None] * length
    # Liste für Matrizen mit rechten
    V = [None] * length
    
    modes = [None] * length
    PCA = [None] * length

    # Berechnen der durchschnittlichen Matrix aller Zeitschritte falls gewünscht
    if meanMatrix:
        meansMatrix = calculate_Mean_Matrix(density_timeseries)    

    # Berechnen der PCA aller Matrizen
    for i in range(0, len(density_timeseries)):
        matrix = density_timeseries[i]
        if meanMatrix:
            matrix = matrix - meansMatrix
        U[i], s[i], V[i], modes[i] = PCA_just_Decomposition(matrix, keepPercentage, centerMatrix)
    if(keepModes != 0):
        mode = keepModes
    else:
        mode = np.max(modes)
    PCA = PCA_with_Max_Modes(U, s, V, mode, recombine)
    #PCA[i] = np.concatenate((np.transpose(U[i]), s[i], V[i]), axis=1)
    
    if(substractTimesteps):
        PCA = substract_Timesteps(PCA)

    if(addTimesteps > 0):
        PCA = add_Timesteps(PCA, addTimesteps)

    if(addMultibleTimesteps > 0):
        PCA = add_Multible_Timesteps(PCA, addMultibleTimesteps)

    return PCA, mode
    # return U, s, V
    

def PCA_with_Max_Modes(U, s, V, maxMode, recombine):
    # Abschneiden der Matrizen bei modes

    PCA = [None] * len(U)
    #maxMode = np.max(modes)
    #maxMode = 10

    for i in range(0, len(U)):
        U[i] = U[i][:, :maxMode]
        S = np.array([s[i][:maxMode]])
        V[i] = V[i][:maxMode, :]

        if(recombine is False):
            PCA[i] = np.concatenate((U[i], S, V[i].T), axis=0)

        if(recombine):
            #Si = np.zeros((maxMode, maxMode), dtype=complex)
            #Si[:maxMode, :maxMode] = np.diag(S)
            Si = np.diag(s[i][:maxMode])
            PCA[i] = np.dot(U[i], np.dot(Si, V[i])).real

        PCA[i] = np.around(PCA[i], 4)
        

    return PCA


def PCA_just_Decomposition(matrix, keepPercentage=99, centerMatrix=False):
    # Berechnen der PCA Zerlegung für eine Matrix bei der keepPercentage der 
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
    
    return U, s, V, modes


def substract_Timesteps(PCA):

    PCA_sub = [None] * (len(PCA) - 1)
    for i in range(0, (len(PCA) - 1)):
        sub = PCA[i+1] - PCA[i]
        PCA_sub[i] = np.concatenate((PCA[i+1], sub), axis=0)
    return PCA_sub


def add_Timesteps(PCA, addTimesteps):

    PCA_add = [None] * (len(PCA) - addTimesteps)
    for i in range(0, (len(PCA) - addTimesteps)):
        add = sum(PCA[i:(i+addTimesteps+1)])
        PCA_add[i] = np.concatenate((PCA[i+addTimesteps], add), axis=0)
    return PCA_add


def add_Multible_Timesteps(PCA, addTimesteps):

    PCA_add = [None] * (len(PCA) - addTimesteps)
    for i in range(0, (len(PCA) - addTimesteps)):
        PCA_add[i] = PCA[i]
        for j in range(2, addTimesteps+2):
            PCA_add[i] = np.concatenate((PCA_add[i], sum(PCA[i:(i+j)])),axis=0)
    return PCA_add


def calculate_Mean_Matrix(density_timeseries):

    meanMatrix = np.mean(density_timeseries, axis=0)
    return meanMatrix


##################################Tests########################################
# Diese Fuktionen führen die selben Aufgaben aus wie die Oberen, jedoch werden 
# hier statt der zerlegten Matrix Bilder der originalen und wieder 
# zusammengesetzten  reduzierten Matrix erzeugt und der durchschnittliche 
# quadratische Fehler berechnet.


def mainPCAtest(density_timeseries, keepPercentage=99, substractTimesteps=False,\
                addTimesteps=0, addMultibleTimesteps=0, centerMatrix=False, \
                meanMatrix=False, recombine=True):
   
   PCA = mainPCA(density_timeseries, keepPercentage=keepPercentage, \
               substractTimesteps=substractTimesteps, \
               addTimesteps=addTimesteps, \
               addMultibleTimesteps=addMultibleTimesteps, \
               centerMatrix=centerMatrix, meanMatrix=meanMatrix, \
               recombine=recombine)

   for i in range(0, len(density_timeseries), 50):
       plot_density(density_timeseries[i], (str(i) + "_****"), "Orginal")
       plot_density(PCA[i], (str(i) + "_PCAreduced****"), ("_" + str(keepPercentage)))
       mse = ((density_timeseries[i] - PCA[i]) ** 2).mean(axis=None)

   return mse
   # return U, s, V

