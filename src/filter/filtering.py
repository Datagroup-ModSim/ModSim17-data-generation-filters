import numpy as np

def thresholding(densityMatrix):

    densityMatrix = densityMatrix*100
    maxVal = densityMatrix.max()
    densityMatrix =  densityMatrix/maxVal


    return None