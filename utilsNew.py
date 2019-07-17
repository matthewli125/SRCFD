import re
from os import listdir, path
import shutil
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import cv2
import h5py
from mpl_toolkits.mplot3d import Axes3D
import moviepy.editor as mpy
from time import sleep

PTHd = listdir("D:/openfoamData/ff")
PTH = "D:/openfoamData/ff"
msh = "/system/blockMeshDict"
HRSAVEPTH = "D:/openfoamData/newcodedata/highres/"
LRSAVEPTH = "D:/openfoamData/newcodedata/lowres/"
files = ["alpha.water","p", "p_rgh"]

def copyfiles():
    file1 = "alpha.water.orig"
    file2 = "blockMeshDict"
    for i in range(400):
        shutil.copy(file1, "DB{}_highres/0".format(i))
        shutil.copyfile(file2, "DB{}_highres/system/blockMeshDict".format(i))

def countTimes():
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

def checkComplete(pth):
    i = 0
    for filename in listdir(pth):
        if filename.find("DB{}".format(i)):
            print(filename)
        else:
            continue
        i+=1
    print("done")

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

def xyzmax(pointList):
    x = max(pointList, key = lambda x: x[0])[0]
    y = max(pointList, key = lambda x: x[1])[1]
    z = max(pointList, key = lambda x: x[2])[2]
    return [x,y,z]

def buildBlock(block, File):
    finalblock = np.empty(block[1])
    finalblock = finalblock.reshape(block[1][1], block[1][0], block[1][2])
    for k in range(block[1][2]):
        for i in reversed(range(block[1][1])):
            for j in range(block[1][0]):
                point = float(File.readline())
                finalblock[i][j][k] = point if point > 0.00001 else 0
    return finalblock

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

def sortbyname(files):
    return sorted([i for i in files], key=lambda x: \
                                    float(x.split("-")[0].split("_")[0])*10 + \
                                    float(x.split("-")[-1].replace(".npy", "")))

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

buildall([32,32,32], True, "D:/openfoamData/ff/")
# overtime_arr = []
# for i in listdir("overtime_data"):
#     a = np.load("D:/openfoamData/overtime_data/"+i)
#     a = a.reshape((32,32))
#     for i in range(32):
#         for j in range(32):
#             if a[i][j] < 0.0001:
#                 a[i][j] = 0
#     overtime_arr.append(a)
# overtime_arr = np.flip(np.array(overtime_arr),1)
# overtime_arr = overtime_arr.transpose(2,0,1)
# fig = plt.figure()
# ax = fig.gca(projection='3d')
# ax.voxels(overtime_arr, facecolors='yellow', edgecolor='black')
