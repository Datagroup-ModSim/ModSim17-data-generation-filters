import csv
from glob import glob
import os
from PIL import Image
from matplotlib import pyplot as plt

from mpl_toolkits.mplot3d import axes3d

#import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import numpy as np

OUTPUT_ROOT_DIRECTORY = os.path.join('../output/100_pos1')  # directory were output files are
INDEX_TIME_STEP = 0
INDEX_PED_ID = 1
INDEX_POS_X = 2
INDEX_POS_Y = 3
INDEX_TARGET_ID = 4
# --------------------------------------------------------
# Test for density data
# --------------------------------------------------------

def get_file_names(directory):
    file_names = []

    for file in glob(directory+"//*.csv"):
        file_names.append(file)
    return file_names

#size = (10,16)
#size = (20,20)
size = (120,100)
#size = (120,100)
#size = (160,80)

def test_density_data():

    file_names = get_file_names(OUTPUT_ROOT_DIRECTORY)

    # plot single file
    tag_file = 1
    for name in file_names:
        data = read_density(name)
        tag_row = 1
        for row in data:
            row = row[0:-3]
            matrix = np.reshape(row,size)
            plot_density(matrix, name, str("_{0}_{1}").format(tag_file,tag_row))
            tag_row+=1

        tag_file+=1
        print("done: ", str(np.round((tag_file / len(file_names)) * 100, 0)), " %")


# read data files into matrix
def read_density(file_dir):
    data = []
    with open(file_dir, 'r') as f:
        csv_reader = csv.reader(f, delimiter=';')

        for line in csv_reader:
            row = []
            for element in line:
                try:
                    row.append(float(element))
                except ValueError:
                    print(element)
            data.append(row)

    return data


def plot_gauss_glocke():

    data = read_density(os.path.join("")) # file liegt nicht auf repo

    data = np.array(data)

    x1 = data.shape[0]
    #x2 = data.shape[1][:][-10]

    l1 = np.linspace(13,66,num=53)
    #l2 = np.linspace(0,x2,num=x2)

    X, Y = np.meshgrid(l1, l1)

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    print(np.shape(data[13:66,13:66]))
    surf = ax.plot_surface(X, Y, data[33:86,13:66], cmap=cm.coolwarm,linewidth=0, antialiased=False)
    np.savetxt("vadere_gaussian.csv",data[33:86,13:66],delimiter=";",fmt='%0.4f')
    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.title("Gaussian")
    plt.show()


def plot_density(data, filename, tag):
    # plot data
    data = np.array(data)
    s = data.shape
    img = Image.new('RGB', s)
    max_data = np.max(data)

    for y in range(0, s[0]):
        for x in range(0, s[1]):
            val = data[y][x]
            bw = np.uint8(255-(val*255)/(max_data))
            img.putpixel((y, x), (bw, bw, bw))

    #img = img.resize((100,160))
    img.save(str("{0}{1}.png").format(filename[:-4],tag))


def plot_trajectories(data):

    for id in data:
        x = np.array(id)
        xx = x[:,INDEX_POS_X]
        xy = x[:,INDEX_POS_Y]
        plt.plot(xx,xy,'-o')
        index = 1
        for step in x:
            plt.text(step[INDEX_POS_X], step[INDEX_POS_Y], str(index), color="blue", fontsize=12)
            index+=1

    plt.savefig("test norm trajectories")
    plt.show()


test_density_data()
