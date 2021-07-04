from random import choice
from os import listdir, path, makedirs
from decimal import Decimal
import shutil
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from foamToPy import buildarr
import h5py
from copy import deepcopy
from mpl_toolkits.mplot3d import Axes3D
import imageio
import moviepy.editor as mpy
from paths import *


#helper for saveh5, sorts a list of files based on timestep and case number
def sortbyname(files):
    return sorted([i for i in files], key=lambda x: \
                                    float(x.split("-")[0].split("_")[0])*10 + \
                                    float(x.split("-")[-1].replace(".npy", "")))

#loads arrays from highres and lowres savepaths and makes an hdf5 dataset file
def saveh5(lrSavepth, hrSavepth):
    FILES = ["alpha.water"]
    for i in FILES:
        lrSortList = sortbyname([x for x in listdir(lrSavepth) if i in x])
        hrSortList = sortbyname([x for x in listdir(hrSavepth) if i in x])
        for i in range(len(lrSortList)):
            print(lrSortList[i], "\t", hrSortList[i])
        h5file = h5py.File("{}new.h5".format(i), "w")
        h5file.create_dataset("lowres", data=[np.load(lrSavepth + x) for x in tqdm(lrSortList)])
        h5file.create_dataset("highres", data=[np.load(hrSavepth + x) for x in tqdm(hrSortList)])
        h5file.close()

#stacks 2d arrays into a single 3d array that represents change over time
def overtime(res, files):
    overtime_arr = []
    for i in files:
        print(i)
        a = np.load(i)
        overtime_arr.append(a)
    return (np.array(overtime_arr))


def overtime_all(OT_lrPth, OT_hrPth, interval, hres=[32,32,1], lres=[16,16,1]):
    lr = [LRSAVEPTH + i for i in sortbyname(listdir(LRSAVEPTH))]
    hr = [HRSAVEPTH + i for i in sortbyname(listdir(HRSAVEPTH))]
    for file in FILES:
        recursive_build(list(filter(lambda x: file == x.split("-")[2], lr)), interval, lres, OT_lrPth, file, 0)
        recursive_build(list(filter(lambda x: file == x.split("-")[2], hr)), interval, hres, OT_hrPth, file, 0)


def recursive_build(lst, interval, res, savepth, file, i):
    if len(lst) < 1: return
    np.save("{}/{}x{}x{}-{}-{}_{}.npy".format(savepth,res[0],res[1],res[2], \
                            file,i,i+interval), overtime(res, lst[0:interval]))
    recursive_build(lst[interval:], interval, res, savepth, file, i+interval)


    plt.show()


def clt(choices, num):
    return choice([j for j in choices if j < Decimal(num) - Decimal(0.01)])


from matrix import pmatrixAvg, matrixNormalize


def extractFeatures(arr, featureSize):
    arr = deepcopy(arr)
    incr = [0,0]
    features = []
    for i in range(0, len(arr), featureSize[0]):
        for j in range(0, len(arr), featureSize[1]):
            avg = pmatrixAvg(arr[i:i+featureSize[0],j:j+featureSize[1]])
            if avg > 0.999999 or avg < 0.000001:
                pass
            else:
                features.append((i//featureSize[0],j//featureSize[1]))
            # features.append((i//featureSize[0],j//featureSize[1]))
    return features


def syncFeatures(arr1, arr2, features, featureSize1, featureSize2):
    features1 = [(i[0]*featureSize1[0], i[1]*featureSize1[1]) for i in features]
    features2 = [(i[0]*featureSize2[0], i[1]*featureSize2[1]) for i in features]

    slices1 = [arr1[i[0]:i[0]+featureSize1[0],i[1]:i[1]+featureSize1[1]] for i in features1]
    slices2 = [arr2[i[0]:i[0]+featureSize2[0],i[1]:i[1]+featureSize2[1]] for i in features2]

    return [[slices1[i],slices2[i],features[i]] for i in range(len(features))]


def timesFromPath(pth):
    ignoreFiles = ["constant", "postProcessing", "system", "0"]
    return [pth+i for i in listdir(pth) if path.isdir(pth+i) and i not in ignoreFiles]

def graph_pair(frame1, frame2):
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16,8))
    axes[0].imshow(frame1)
    axes[1].imshow(frame2)
    
def graph_pair_paths(frame1, frame2):
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16,8))
    axes[0].imshow(np.squeeze(np.load(LRDATAPTH+frame1)))
    axes[1].imshow(np.squeeze(np.load(HRDATAPTH+frame2)))

def gif3(pth, name, res):

    try:
        shutil.rmtree("gifTemp")
        makedirs("gifTemp")
    except:
        pass

    imgs = []
    for i in tqdm([pth + j for j in listdir(pth) if path.isdir(pth + j) and j not in ["constant", "postProcessing", "system", "0"]]):
        water = buildarr(res, i+"/alpha.water", pth+"/system/blockMeshDict")
        pressure = np.squeeze(buildarr(res, i+"/p_rgh", pth+"/system/blockMeshDict"))
        velocity = np.squeeze(buildarr(res, i+"/U", pth+"/system/blockMeshDict"))


        fig, axes = plt.subplots(nrows=1, ncols=3, figsize = (24,8))
        axes[0].imshow(np.squeeze(water))
        axes[1].imshow(np.squeeze(pressure))
        axes[2].imshow(np.squeeze(velocity))
        figname = "gifTemp/{}.jpeg".format(i.split("/")[-1])
        plt.savefig(figname)
        imgs.append(figname)

    imgs = sorted(imgs, key = lambda x: float(x.split("/")[-1].replace(".jpeg", "")))

    clip=mpy.ImageSequenceClip(imgs, fps=24)
    clip.write_gif(name, fps=24)
    shutil.rmtree("gifTemp")


def gifCompare(pth1, pth2, res1, res2, fps, name):
    try:
        makedirs("gifTemp")
        print("dir made")
    except:
        pass

    imgs = []
    for i,j in tqdm(list(zip(timesFromPath(pth1), timesFromPath(pth2)))):
        water1 = buildarr(res1, i+"/alpha.water", pth1+"/system/blockMeshDict")
        pressure1 = np.squeeze(buildarr(res1, i+"/p_rgh", pth1+"/system/blockMeshDict"))
        velocity1 = np.squeeze(buildarr(res1, i+"/U", pth1+"/system/blockMeshDict"))

        water2 = buildarr(res2, j+"/alpha.water", pth2+"/system/blockMeshDict")
        pressure2 = np.squeeze(buildarr(res2, j+"/p_rgh", pth2+"/system/blockMeshDict"))
        velocity2 = np.squeeze(buildarr(res2, j+"/U", pth2+"/system/blockMeshDict"))

        fig, axes = plt.subplots(nrows=3, ncols=2, figsize = (16,24))
        axes[0][0].imshow(np.squeeze(water1))
        axes[0][1].imshow(np.squeeze(water2))
        axes[1][0].imshow(np.squeeze(pressure1))
        axes[1][1].imshow(np.squeeze(pressure2))
        axes[2][0].imshow(np.squeeze(velocity1))
        axes[2][1].imshow(np.squeeze(velocity1))
        figname = "gifTemp/{}.jpeg".format(i.split("/")[-1])
        plt.savefig(figname)
        imgs.append(figname)

    imgs = sorted(imgs, key = lambda x: float(x.split("/")[-1].replace(".jpeg", "")))

    clip=mpy.ImageSequenceClip(imgs, fps=fps)
    clip.write_gif(name, fps=fps)
    shutil.rmtree("gifTemp")

def verifyFeaturePatches(featurePatches, res1, res2):
    fullArr1 = np.zeros((256,256))
    fullArr2 = np.zeros((512,512))

    for i in featurePatches:
        pos = [i[2][x] * res1[x] for x in range(2)]
        fullArr1[ \
                pos[0]:pos[0]+res1[0], \
                pos[1]:pos[1]+res1[1]  \
                ] = np.squeeze(i[0])

    for i in featurePatches:
        pos = [i[2][x] * res2[x] for x in range(2)]
        fullArr2[ \
                pos[0]:pos[0]+res2[0], \
                pos[1]:pos[1]+res2[1]  \
                ] = np.squeeze(i[1])

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16,8))
    axes[0].imshow(fullArr1)
    axes[1].imshow(fullArr2)
    plt.show()

if __name__ == "__main__":
    # gif3(PTH+"/1/", "1-256x256x1.gif", [256,256,1])
    # gif3(PTH+"/1_highres/", "1-512x512x1.gif", [512,512,1])
    LRList = sortbyname([i for i in listdir(LRDATAPTH)])
    HRList = sortbyname([i for i in listdir(HRDATAPTH)])

    ##Verify that corresponding entries are matched correctly
    for i in tqdm(range(len(HRList))):
        LRCaseStep = [LRList[i].split("\\")[-1].split("-")[0], LRList[i].split("\\")[-1].split("-")[-1]]
        HRCaseStep = [HRList[i].split("\\")[-1].split("-")[0].split("_")[0], HRList[i].split("\\")[-1].split("-")[-1]]

        if LRCaseStep != HRCaseStep:
            print("\n\n",LRCaseStep, HRCaseStep)
            raise ValueError

    print("\ncases and timesteps synced\n")

    for i in tqdm(range(len(HRList))):
        LRCaseStep = [LRList[i].split("\\")[-1].split("-")[0], LRList[i].split("\\")[-1].split("-")[-1]]
        LRarr = np.load(LRDATAPTH + LRList[i])
        HRarr = np.load(HRDATAPTH + HRList[i])
        print(LRDATAPTH + LRList[i], HRDATAPTH + HRList[i])

        features = extractFeatures(HRarr,[64,64])
        featurePatches = syncFeatures(LRarr, HRarr, features, [32,32], [64,64])

        if i%50 == 0:
            verifyFeaturePatches(featurePatches, [32,32], [64,64])

        newDir = DATAPTH + "/featurePatches/" + "{}--".format(i) + "-".join(map(str,LRCaseStep))
        # makedirs(newDir)
        #
        # for j in featurePatches:
        #     np.save(newDir + "/" + "-".join(map(str, j[2])) + ".npy", j[0])
        #     np.save(newDir + "/" + "-".join(map(str, j[2])) + "-HR" + ".npy", j[1])
