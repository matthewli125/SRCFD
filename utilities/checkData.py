import re
from os import listdir, path, system
import shutil
import numpy as np
import matplotlib.pyplot as plt
import cv2
import h5py
from random import randint
from paths import LRDATAPTH, HRDATAPTH
from tqdm import tqdm

data = h5py.File("D:/projects/SRCFD/utilities/alpha.waternew.h5")
start = randint(0,800)
start = 61*start+56

def checkData(data, start):
    lr = [data["lowres"][i] for i in range(start, start+5)]
    # lr = [data["lowres"][i] for i in range(start-5, start)]
    hr = [data["highres"][i] for i in range(start, start+5)]

    fig, axes = plt.subplots(nrows=5, ncols=2, figsize=(8,8))
    for i in range(5):
        axes[i][0].imshow(np.squeeze(lr[i]))
        axes[i][1].imshow(np.squeeze(hr[i]))
        # axes[i][0].imshow(np.squeeze(np.load("D:/openfoamData/newcodedata2/lowres/236-16x16x1-alpha.water-0.75.npy")))
        # axes[i][1].imshow(np.squeeze(np.load("D:/openfoamData/newcodedata2/highres/236_highres-32x32x1-alpha.water-0.75.npy")))
        fig.show()
        plt.show()

def checkFields(lrDest, hrDest, num):
    for i in tqdm(range(num)):
        lrFile = open(lrDest.format(i) + setFieldsDictPath, 'r')
        hrFile = open(hrDest.format(i) + setFieldsDictPath, 'r')
        waterSizeLR = lrFile.readlines()[26]
        waterSizeHR = hrFile.readlines()[26]
        if waterSizeLR != waterSizeLR:
            print(i,waterSizeLR, waterSizeHR)
        lrFile.close()
        hrFile.close()

def checkDataOrder(file, num):
    data = h5py.File(file, "r")
    LR = data["lowres"]
    HR = data["highres"]
    size = len(HR)
    fig, axes = plt.subplots(nrows=2, ncols=num, figsize = (5,5))
    for i in range(num):
        index = randint(0,size)
        axes[0,i].imshow(np.squeeze(LR[index][0]))
        axes[0,i].set_title(LR[index][1])
        axes[1,i].imshow(np.squeeze(HR[index][0]))
        axes[1,i].set_title(HR[index][1])
