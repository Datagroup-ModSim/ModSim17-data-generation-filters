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
from src.util.helper import group_by_pedestrian_id, extract_observation_area

OUTPUT_ROOT_DIRECTORY = os.path.join('../output/0.02-0.35-0.63_Distribution_2017-11-19_19-16-09.90')  # directory were output files are
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

    for file in glob(directory+"//*.trajectories"):
        file_names.append(file)
    return file_names

#size = (10,16)
#size = (20,20)
#size = (120,100)
#size = (120,100)
size = (160,80)

def test_density_data():

    file_names = get_file_names(OUTPUT_ROOT_DIRECTORY)

    # plot single file
    tag_file = 1
    for name in file_names:
        data = read_datafile(name)
        tag_row = 1
        for row in data:
            row = row[0:-3]
            matrix = np.reshape(row,size)
            plot_density(matrix, name, str("_{0}_{1}").format(tag_file,tag_row))
            tag_row+=1

        print("done: ", str(np.round((tag_file / len(file_names)) * 100, 0)), " %")
        tag_file += 1

def test_trajectories_data():
    file_names = get_file_names(OUTPUT_ROOT_DIRECTORY)

    tag_file = 1
    for name in file_names:
        data = read_datafile(name)
        plot_trajectories(data)

        print("done: ", str(np.round((tag_file / len(file_names)) * 100, 0)), " %")
        tag_file += 1


def test_formatted_trajectories_data():
    file_names = get_file_names(OUTPUT_ROOT_DIRECTORY)

    tag_file = 1
    for name in file_names:
        data = read_datafile(name)
        tag_ped = 1
        for row in data:
            plot_formatted_trajectories(row[0:-1],row[-1])

            plt.xlabel("x")
            plt.ylabel("y")
            plt.savefig("Plots/trajectories_formatted_{0}.png".format(tag_file))
            tag_ped+=1
            if tag_ped > 10:
                break
        print("done: ", str(np.round((tag_file / len(file_names)) * 100, 0)), " %")
        tag_file += 1


# read data files into matrix
def read_datafile(file_dir):
    data = []
    with open(file_dir, 'r') as f:
        csv_reader = csv.reader(f, delimiter=' ')

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

    data = read_datafile(os.path.join("")) # file liegt nicht auf repo

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

    img = img.resize((size[0]*10,size[1]*10))
    img.save(str("{0}{1}.png").format(filename[:-4],tag))


def plot_formatted_trajectories(row, targetid):
    color = get_target_color(targetid)
    x = []
    y = []
    for i in range(0,len(row)):
        if i%2 == 0:
            x.append(row[i])
        else:
            y.append(row[i])

    plt.plot(x,y,'-o', c=color)
    for i in range(0,len(x)):
        plt.text(x[i],y[i],str(i))


def plot_trajectories(data):
    data = sorted(data, key=lambda row: row[INDEX_PED_ID])
    data_camera = extract_observation_area(data,[20,10,10,10])
    data_id = group_by_pedestrian_id(data_camera)
    tag_ped = 1
    for ped in data_id:
        target_id = ped[INDEX_PED_ID][-1]
        color = get_target_color(target_id)
        x = np.array(ped)
        xx = x[:,INDEX_POS_X]
        xy = x[:,INDEX_POS_Y]
        plt.plot(xx,xy,'-o', c=color)

        for i in range(0, len(xx)):
            plt.text(xx[i], xy[i], str(i))

        tag_ped += 1
        if tag_ped > 10:
            break


    plt.xlabel("x")
    plt.ylabel("y")
    plt.savefig("Plots/trajectories{0}.png".format(tag_ped))




def get_target_color(targetid):
    if targetid == 0 or targetid == 4:
        return 'blue'
    if targetid == 1 or targetid == 5:
        return 'red'
    if targetid == 2 or targetid == 6:
        return 'green'

#test_density_data()
#test_formatted_trajectories_data()
test_trajectories_data()