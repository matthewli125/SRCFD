import os
from os import listdir
import shutil
import numpy as np
from tempfile import TemporaryFile
import matplotlib.pyplot as plt
from pathlib import Path
import cv2


# This is the old utils code that I wrote a while ago. A lot of the functions in here were rushed and basically hard-coded,
# and have been replace with much better code in the new utils.py file. I kept this file here to serve as a point of comparison
# to my new code as well as to show an example of poor coding practices. 


def removelogs(res):
    if res == "high":
        current = 0
        for filename in os.listdir():
            for filename in os.listdir("DB{}_highres".format(current)):
                if (filename == "log.blockMesh") or (filename == "log.interFoam") or (filename == "log.setFields"):
                    try:
                        os.remove("DB{}_highres/".format(current) + filename)
                        print("DB{}_highres cleaned!".format(current))
                    except OSError:
                        pass
            if current < 399:
                current+=1
    elif res == "low":
        current = 0
        for filename in os.listdir():
            for filename in os.listdir("DB{}".format(current)):
                if (filename == "log.blockMesh") or (filename == "log.interFoam") or (filename == "log.setFields"):
                    try:
                        os.remove("DB{}/".format(current) + filename)
                        print("DB{} cleaned!".format(current))
                    except OSError:
                        pass
            if current < 399:
                current+=1
    
def copyfiles():
    file1 = "alpha.water.orig"
    file2 = "blockMeshDict"
    for i in range(400):
        shutil.copy(file1, "DB{}_highres/0".format(i))
        shutil.copyfile(file2, "DB{}_highres/system/blockMeshDict".format(i))

def allClean():
    for i in range(400):
        for filename in os.listdir("DB{}".format(i)):
            if (filename != "0") and (filename !="constant") and (filename != "system") and (filename != "Allclean") and (filename != "Allrun"):
                try:
                    shutil.rmtree("DB{}/{}".format(i, filename))
                except OSError:
                    pass
        try:
            shutil.rmtree("DB{}/constant/polyMesh".format(i))
        except OSError:
            pass
        print("case DB{} has been successfully cleaned".format(i))
    removelogs()


def countTimes():
    done = 0
    for i in range(400):
        count = 0
        for filename in os.listdir("DB{}_highres".format(i)):
            count+=1
        print("DB{}_highres has {} timesteps".format(i, count))
    for i in range(400):
        count = 0    
        for filename in os.listdir("DB{}".format(i)):
            count+=1
        if count !=109:
            print("DB{} has {} timesteps".format(i, count))
            done +=1
    print("{} are done cleaning.".format(done))

def checkComplete():
    i = 0
    for filename in os.listdir(os.getcwd()):
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
        for filename in os.listdir("DB{}".format(i)):
            count+=1
        if count < 108:
            incomplete.append(i)
    for i in incomplete:
        out+="(rm DB{}/log.interFoam && cd DB{} && interFoam) & ".format(i, i)
    return out

def plotxyz(num, time, res = "high"):
    if res == "high":
        with open("DB0_highres/0/Cx", "r") as file:
            X = file.readlines()[23:1043]
            X = list(map(lambda x: float(x), X))
        file.close()
        with open("DB0_highres/0/Cy", "r") as file:
            Y = file.readlines()[23:1043]
            Y = list(map(lambda x: float(x), Y))
        file.close()
        with open("DB{}_highres/{}/alpha.water".format(num, time), "r") as file:
            Z = file.readlines()[23:1043]
            Z = list(map(lambda x: float(x)*400 + 1, Z))
        file.close()
    elif res == "low":
        with open("DB0/5/Cx", "r") as file:
            X = file.readlines()[23:278]
            X = list(map(lambda x: float(x), X))
        file.close()
        with open("DB0/5/Cy", "r") as file:
            Y = file.readlines()[23:278]
            Y = list(map(lambda x: float(x), Y))
        file.close()
        with open("DB{}/{}/alpha.water".format(num, time), "r") as file:
            Z = file.readlines()[23:278]
            Z = list(map(lambda x: float(x)*400 + 1, Z))
        file.close()

    plt.scatter(X, Y, Z)
    plt.show()

def plotxy(res = "high"):
    if res == "high":
        with open("DB0_highres/5/Cx",  "r") as file:
            X = file.readlines()[23:1043]
            X = list(map(lambda x: float(x), X))
        file.close()
        with open("DB0_highres/5/Cy", "r") as file:
            Y = file.readlines()[23:1043]
            Y = list(map(lambda x: float(x), Y))
        file.close()
    elif res == "low":
        with open("DB0/5/Cx", "r") as file:
            X = file.readlines()[23:278]
            X = list(map(lambda x: float(x), X))
        file.close()
        with open("DB0/5/Cy", "r") as file:
            Y = file.readlines()[23:278]
            Y = list(map(lambda x: float(x), Y))
        file.close()
        
    plt.scatter(X, Y)
    plt.show()

def saveallhighres():
    for i in range(0,400):
        try:
            savehighres(i, "alpha.water", False)
        except ValueError:
            print("{} water failed".format(i))
            pass
        try:
            savehighres(i, "p", False)
        except ValueError:
            print("{} p failed".format(i))
            pass
        try:
            savehighres(i, "p_rgh", False)
        except ValueError:
            print("{} p_rgh failed".format(i))
            pass
        
def saveallLowres():
    for i in range(0,400):
        try:
            savelowres(i, "alpha.water", False)
        except ValueError:
            print("{} water failed".format(i))
            pass
        try:
            savelowres(i, "p", False)
        except ValueError:
            print("{} p failed".format(i))
            pass
        try:
            savelowres(i, "p_rgh", False)
        except ValueError:
            print("{} p_rgh failed".format(i))
            pass
        
    
def savehighres(num, filename, plot):
    for j in range(5, 501, 5):
        array = np.zeros(shape = [32,32])
        if int(j/100) == j/100:
            a = int(j/100)
        else:
            a = j/100

        if Path("D:/openfoamData/{}_highres/DB{}_highres_{}_@time = {}.npy".format(filename, num, filename, a)).exists():
            print("{} {} {} already exists".format(filename, num, a))
            return
        
        with open("DB{}_highres/{}/{}".format(num, a, filename), 'r') as file:
            water = file.readlines()[23:1043]
            water = list(map(lambda x: float(x), water))
            #print(water[0])
        file.close()


        for i in range(2):
            array[31-i][:16] = water[i*16: i*16+16]
        
        for i in range(2):
            array[31-i][18:] = water[i*14+32: i*14+14+32]

        for i in range(0,29):
            array[31-i-2][:16] = water[i*16+32+28 : i*16+16+32+28]

        for i in range(0,29):
            array[31-i-2][16:18] = water[i*2+32+28+30*16:i*2+2+ 32+28+30*16]

        for i in range(0,29):
            array[31-i-2][18:] = water[i*14+32+28+30*16+30*2:i*14+14+32+28+30*16+30*2]
        if plot == True:
            plt.imshow(array)
            plt.savefig("plots//highres{}_DB{}_highres_{}_{}.png".format(j,num, filename, a))
        np.save("D:/openfoamData/{}_highres/DB{}_highres_{}_@time = {}.npy".format(filename, num, filename, a), array)


from scipy import misc

def savelowres(num, filename, plot):
    for j in range(5, 501, 5):
        array = np.zeros(shape = [16,16])
        if int(j/100) == j/100:
            a = int(j/100)
        else:
            a = j/100

##        if Path("D:/openfoamData/{}_lowres/DB{}_{}_@time = {}.npy".format(filename, num, filename, a)).exists():
##            print("{} {} {} already exists".format(filename, num, a))
##            return
        
        with open("DB{}/{}/{}".format(num, a, filename), 'r') as file:
            water = file.readlines()[23:278]
            water = list(map(lambda x: float(x), water))
            #print(water[0])
        file.close()
        #print(Path("D:/openfoamtData/{}_lowres/DB{}_{}_@time = {}.npy".format(filename, num, filename, a)))
        
        for i in range(1):
            array[15-i][:8] = water[i*8: i*8+8]
        
        for i in range(1):
            array[15-i][9:] = water[i*7+8: i*7+7+8]

        for i in range(0,14):
            array[15-i-1][:8] = water[i*8+8+7:i*8+8+8+7]

        for i in range(0,14):
            array[15-i-1][8] = water[i+8+7+15*8]

        for i in range(0,14):
            array[15-i-1][9:] = water[i*7+8+7+15*8+15: i*7+7+8+7+15*8+15]
        #array = misc.imresize(array, 2.0, 'bicubic')
        #array = cv2.resize(array, (32, 32), interpolation = cv2.INTER_CUBIC)
        if plot == True:
            plt.imshow(array)
            plt.savefig("plots/lowres/{}_DB{}_{}_{}.png".format(j,num, filename, a))
        
        np.save("D:/openfoamData/{}_lowres/DB{}_{}_@time = {}.npy".format(filename, num, filename, a), array)

import h5py

def saveh5():
    temp = 0
    waterLowres = []
    waterHighres = []
    pLowres = []
    pHighres = []
    p_rghLowres = []
    p_rghHighres = []

    for file in listdir("D:/openfoamData/alpha.water_highres"):
        temp = np.load("D:/openfoamData/alpha.water_highres/" + file)
        print(file)
        print(temp.shape)
        temp = temp.reshape(32, 32, 1)
        waterHighres.append(temp)
        
    for file in listdir("D:/openfoamData/alpha.water_lowres"):
        temp = np.load("D:/openfoamData/alpha.water_lowres/" + file)
        print(file)
        print(temp.shape)
        temp = temp.reshape(32, 32, 1)
        waterLowres.append(temp)

    for file in listdir("D:/openfoamData/p_highres"):
        temp = np.load("D:/openfoamData/p_highres/" + file)
        temp = temp.reshape(32, 32, 1)
        pHighres.append(temp)
        
    for file in listdir("D:/openfoamData/p_lowres"):
        temp = np.load("D:/openfoamData/p_lowres/" + file)
        temp = temp.reshape(32, 32, 1)
        pLowres.append(temp)

    for file in listdir("D:/openfoamData/p_rgh_highres"):
        temp = np.load("D:/openfoamData/p_rgh_highres/" + file)
        temp = temp.reshape(32, 32, 1)
        p_rghHighres.append(temp)
        
    for file in listdir("D:/openfoamData/p_rgh_lowres"):
        temp = np.load("D:/openfoamData/p_rgh_lowres/" + file)
        temp = temp.reshape(32, 32, 1)
        p_rghLowres.append(temp)

    waterLowres = np.asarray(waterLowres)
    waterHighres = np.asarray(waterHighres)
    h5water = h5py.File("water_large.h5", "w")
    h5water.create_dataset("highres", data = waterHighres)
    h5water.create_dataset("lowres", data = waterLowres)
    h5water.close()
    
    pLowres = np.asarray(pLowres)
    pHighres = np.asarray(pHighres)
    h5p = h5py.File("p_large.h5", "w")
    h5p.create_dataset("highres", data = pHighres)
    h5p.create_dataset("lowres", data = pLowres)
    h5p.close()
    
    p_rghLowres = np.asarray(p_rghLowres)
    p_rghHighres = np.asarray(p_rghHighres)
    h5p_rgh = h5py.File("p_rgh_large.h5", "w")
    h5p_rgh.create_dataset("highres", data = p_rghHighres)
    h5p_rgh.create_dataset("lowres", data = p_rghLowres)
    h5p_rgh.close()
    

def saveh5small():
    temp = 0
    waterLowres = []
    waterHighres = []
    pLowres = []
    pHighres = []
    p_rghLowres = []
    p_rghHighres = []

    for file in listdir("D:/openfoamData/alpha.water_highres_small"):
        temp = np.load("D:/openfoamData/alpha.water_highres_small/" + file)
        print(file)
        print(temp.shape)
        temp = temp.reshape(32, 32, 1)
        waterHighres.append(temp)
        
    for file in listdir("D:/openfoamData/alpha.water_lowres_small"):
        temp = np.load("D:/openfoamData/alpha.water_lowres_small/" + file)
        print(file)
        print(temp.shape)
        temp = temp.reshape(32, 32, 1)
        waterLowres.append(temp)

    for file in listdir("D:/openfoamData/p_highres_small"):
        temp = np.load("D:/openfoamData/p_highres_small/" + file)
        temp = temp.reshape(32, 32, 1)
        pHighres.append(temp)
        
    for file in listdir("D:/openfoamData/p_lowres_small"):
        temp = np.load("D:/openfoamData/p_lowres_small/" + file)
        temp = temp.reshape(32, 32, 1)
        pLowres.append(temp)

    for file in listdir("D:/openfoamData/p_rgh_highres_small"):
        temp = np.load("D:/openfoamData/p_rgh_highres_small/" + file)
        temp = temp.reshape(32, 32, 1)
        p_rghHighres.append(temp)
        
    for file in listdir("D:/openfoamData/p_rgh_lowres_small"):
        temp = np.load("D:/openfoamData/p_rgh_lowres_small/" + file)
        temp = temp.reshape(32, 32, 1)
        p_rghLowres.append(temp)

    waterLowres = np.asarray(waterLowres)
    waterHighres = np.asarray(waterHighres)
    h5water = h5py.File("water_small.h5", "w")
    h5water.create_dataset("highres", data = waterHighres)
    h5water.create_dataset("lowres", data = waterLowres)
    h5water.close()
    
    pLowres = np.asarray(pLowres)
    pHighres = np.asarray(pHighres)
    h5p = h5py.File("p_small.h5", "w")
    h5p.create_dataset("highres", data = pHighres)
    h5p.create_dataset("lowres", data = pLowres)
    h5p.close()
    
    p_rghLowres = np.asarray(p_rghLowres)
    p_rghHighres = np.asarray(p_rghHighres)
    h5p_rgh = h5py.File("p_rgh_small.h5", "w")
    h5p_rgh.create_dataset("highres", data = p_rghHighres)
    h5p_rgh.create_dataset("lowres", data = p_rghLowres)
    h5p_rgh.close()
    
    
    ##new stuff
import re
from functools import reduce


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


def blockStart(pointList):
    x = min(pointList, key = lambda x: x[0])[0]
    y = max(pointList, key = lambda x: x[1])[1]
    z = min(pointList, key = lambda x: x[2])[2]
    return [x,y,z]


def buildBlock(block, File):
    finalblock = np.empty(block[1])
    finalblock = finalblock.reshape(block[1][1], block[1][0], block[1][2])
    for k in range(block[1][2]):
        for i in reversed(range(block[1][1])):
            for j in range(block[1][0]):
                finalblock[i][j][k] = float(File.readline())
    return finalblock


res = np.array([16,16,1])

final = np.zeros([16,16,1])

asdf = open("DB360/0.1/alpha.water", "r")
fdsa = open("DB360/system/blockMeshDict", "r")

points = getVertices(fdsa)
XYZmax = np.array(xyzmax(points))
mul = np.divide(res, XYZmax)
print(mul)
mul = list(map(int, mul))
points = list(map(lambda x: (x[0]*mul[0], x[1]*mul[1], x[2]*mul[2]), points))
points = [map(int, sub) for sub in points]
points = list(map(list, points))
blocks = getBlocks(fdsa, points)
for i in range(23):
    discard = asdf.readline()
for i in range(len(blocks)):
    st = blockStart(blocks[i][0])
    st[0]=res[0]-st[0]
    print(st)
    
    blocks[i] = buildBlock(blocks[i], asdf)
    shp = blocks[i].shape
    #print(shp)
    #final[st[0]:st[0]+shp[0], st[1]:st[1]+shp[1], st[2]:st[2]+shp[2]] = blocks[i]
