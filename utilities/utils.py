import re
from os import listdir, path
import shutil
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import cv2
import h5py
from mpl_toolkits.mplot3d import Axes3D
import imageio
import moviepy.editor as mpy
from time import sleep

# Modify these global vars to the paths and files that you want--PTH is the
# folder with the cases and PTHd is a list of all the folders in PTH
PTHd = []
PTH = "D:/openfoamData/ff"
msh = "/system/blockMeshDict"
HRSAVEPTH = "D:/openfoamData/newcodedata/highres/"
LRSAVEPTH = "D:/openfoamData/newcodedata/lowres/"
files = ["alpha.water","p", "p_rgh"]

def copyfiles(): #copy alpha.water.orig and blockMeshDict to all directories
    file1 = "alpha.water.orig"
    file2 = "blockMeshDict"
    for i in range(400):
        shutil.copy(file1, "DB{}_highres/0".format(i))
        shutil.copyfile(file2, "DB{}_highres/system/blockMeshDict".format(i))

def countTimes(): #counts the number of items in each folder,
    done = 0
    for i in range(400):
        count = 0
        for filename in listdir("DB{}_highres".format(i)):
            count+=1
        print("DB{}_highres has {} timesteps".format(i, count))
    for i in range(400):
        count = 0
        for filename in listdir("DB{}".format(i)):
            count+=1
        if count !=109:
            print("DB{} has {} timesteps".format(i, count))
            done +=1
    print("{} are done cleaning.".format(done))

def checkComplete(pth): #prints out all folders in order to see if all are there
    i = 0
    for filename in listdir(pth):
        if filename.find("DB{}".format(i)):
            print(filename)
        else:
            continue
        i+=1
    print("done")

#finds incomplete cases and generates a bash command that reruns the solver on
# the incomplete cases
def cleanup():
    incomplete = []
    out = ""
    for i in range(400):
        count= 0
        for filename in listdir("DB{}".format(i)):
            count+=1
        if count < 108:
            incomplete.append(i)
    for i in incomplete:
        out+="(rm DB{}/log.interFoam && cd DB{} && interFoam) & ".format(i, i)
    return out

#gets the vertices from the blockMeshDict file and makes a list of tuples, the
#list index of each vertex will correspond to its vertex number
def getVertices(File):
    points = []
    line = ""
    while line != "vertices\n":
        line = File.readline()
    line = File.readline()
    while line != ");\n":
        line = File.readline()
        if len(line)>4: points.append(eval(line[4:].replace(" ", ",")))
    return points

#gets the blocks from the blockMeshDict file, creates a list of blocks, which
#are sets of numbers corresponding to vertices
def getBlocks(File, points):
    blocks = []
    line = ""
    while line != "blocks\n":
        line = File.readline()
    line= File.readline()
    while line != ");\n":
        line = File.readline()
        filtered = re.split('\(|\)', line[4:])
        if len(filtered)<4: break
        Vertices = eval("[" + filtered[1].replace(" ", ",") + "]")
        Vertices = list(map(lambda x: points[x], Vertices))
        Density = eval("[" + filtered[3].replace(" ", ",") + "]")
        blocks.append((Vertices, Density))
    return blocks

def xyzmax(pointList): #gets the largest xyz values from all vertices
    x = max(pointList, key = lambda x: x[0])[0]
    y = max(pointList, key = lambda x: x[1])[1]
    z = max(pointList, key = lambda x: x[2])[2]
    return [x,y,z]

def buildBlock(block, File): #builds a block from data points in a file
    finalblock = np.empty(block[1])
    finalblock = finalblock.reshape(block[1][1], block[1][0], block[1][2])
    for k in range(block[1][2]):
        for i in reversed(range(block[1][1])):
            for j in range(block[1][0]):
                point = float(File.readline())
                finalblock[i][j][k] = point if point > 0.00001 else 0
    return finalblock

#builds all the blocks in a given case into a single array, works for both 2d
#and 3d cases; does array arithmetic based on xyzmax and res (point density)
def buildarr(res, datafile, meshfile):
    final = np.zeros(res)
    data = open(datafile, "r")
    mesh = open(meshfile, "r")
    points = getVertices(mesh)
    XYZmax = np.array(xyzmax(points))
    mul = list(map(int, np.divide(res, XYZmax)))
    blocks = getBlocks(mesh, points)
    for i in range(23):
        discard = data.readline()
    for i in range(len(blocks)):
        st = blocks[i][0][0]
        st = (st[1]*mul[1], st[0]*mul[0], st[2]*mul[2])
        st = list(map(int, st))
        blocks[i] = buildBlock(blocks[i], data)
        shp = blocks[i].shape
        final[res[0]-(st[0]+shp[0]):res[0]-st[0], st[1]:st[1]+shp[1], \
                                          st[2]:st[2]+shp[2]] = blocks[i]
    return final

#performs buildarr on all cases in a directory, but sorts each level based on
#filename so they are saved and named in the correct time and case order. Uses
#global path vars. Set high to true if doing highres to follow file naming
#convention.
def buildall(res, high, savepth):
    filFunc = lambda x: "highres" in x if high else "highres" not in x
    for i in sorted(filter(filFunc, PTHd), key= lambda x: int(x.split("_")[0])):
        print("doing case {} {}\n".format(i, "highres" if high else "lowres"))
        for j in tqdm(list(filter(lambda x:x[0].isdigit(),listdir(PTH+"/"+i)))):
            for k in filter(lambda x: x in files, listdir(PTH+"/"+i+"/"+j)):
                try:
                    arr = buildarr(res, PTH+"/"+i+"/"+j+"/"+k, PTH+"/"+i+msh)
                    np.save(savepth+"{}-{}x{}x{}-{}-{}.npy".format \
                                                        (i, *res, k, j), arr)
                except:
                    pass

#helper for saveh5, sorts a list of files based on timestep and case number
def sortbyname(files):
    return sorted([i for i in files], key=lambda x: \
                                    float(x.split("-")[0].split("_")[0])*10 + \
                                    float(x.split("-")[-1].replace(".npy", "")))

#loads arrays from highres and lowres savepaths and makes an hdf5 dataset file
def saveh5(lrSavepth, hrSavepth):
    lrSortList = sortbyname(listdir(lrSavepth))
    hrSortList = sortbyname(listdir(hrSavepth))
    Data = {}
    for i in tqdm(files):
        print(i)
        h5file = h5py.File("newcodeh5data/{}.h5".format(i), "w")
        h5file.create_dataset("lowres", data=[np.load(lrSavepth+X) for X in \
                tqdm(list(filter(lambda x: i == x.split("-")[2], lrSortList)))])
        h5file.create_dataset("highres", data=[np.load(hrSavepth+X) for X in \
                tqdm(list(filter(lambda x: i == x.split("-")[2], hrSortList)))])
        h5file.close()

#stacks 2d arrays into a single 3d array that represents change over time
def overtime(res, files, path, color):
    overtime_arr = []
    for i in sortbyname(files):
        a = np.load(path + i)
        a = np.squeeze(a)
        for i in range(res[0]):
            for j in range(res[1]):
                if a[i][j] < 0.0001:
                    a[i][j] = 0
                else:
                    a[i][j] = 1
        overtime_arr.append(a)
    overtime_arr = np.flip(np.array(overtime_arr),1)
    overtime_arr = overtime_arr.transpose(2,0,1)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.voxels(overtime_arr, facecolors=color, edgecolor='black')
    ax.set_xlim(0,32)
    ax.set_ylim(0,32)
    ax.set_zlim(0,32)
    plt.show()
    plt.close()
    return overtime_arr
