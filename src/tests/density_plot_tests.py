import csv
from glob import glob
import os
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm


# --------------------------------------------------------
# Test for density data
# --------------------------------------------------------

def get_file_names(directory):
    os.chdir(directory)
    file_names = []

    for file in glob("*.csv"):
        file_names.append(file)
    return file_names

def test_density_data(file_dir, resize):

    file_names = get_file_names(file_dir)

    # plot single file
    for name in file_names:
        data = read_density(file_dir + name)
        plot_gauss_glocke(data)
        #plot_density(data, file_dir, name, resize)


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


def plot_gauss_glocke(data):

    data = np.array(data)

    x1 = data.shape[0]
    x2 = data.shape[1]

    l1 = np.linspace(0,x1,num=x1)
    l2 = np.linspace(0,x2,num=x2)

    X, Y = np.meshgrid(l1, l2)

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    surf = ax.plot_surface(X, Y, data, cmap=cm.coolwarm,linewidth=0, antialiased=False)
    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.title("Gaussian")
    plt.show()


def plot_density(data, file_dir, filename, resize):
    # plot data
    data = np.array(data)
    s = data.shape
    img = Image.new('RGB', s)

    max_data = np.max(data)

    for i in range(0, s[0]):
        for j in range(0, s[1]):
            val = data[i][j]
            bw = np.uint8(255-(val*255)/(max_data) )
            img.putpixel((j, i), (bw, bw, bw))

    if resize:
        img = img.resize((s[0] * 10, s[1] * 10))

    img.save(str(file_dir + "{0}.png").format(filename[:-4]))