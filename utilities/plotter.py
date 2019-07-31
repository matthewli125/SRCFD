from os import listdir, path
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import moviepy.editor as mpy

def plot2d(filelist, savepth):
    count = 0
    # for file in [path.abspath(i.replace("\n", "")) for i in filelist]:
    for file in sortbyname([i.replace("\n", "") for i in filelist]):
        plt.imshow(np.squeeze(np.load(file)))
        print(savepth+"{}-{}.jpg".format(path.basename(file).replace(".npy", ""), count))
        plt.savefig(savepth+"{}-{}.jpg".format(path.basename(file).replace(".npy", ""), count))
        plt.close()
        count+=1

def plot3d(filelist, savepth, color, transpose): #transpose (2,1,0) for 3d, (2,0,1) for over_time
    count = 0
    for file in sortbyname([i.replace("\n", "") for i in filelist]):
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        a = np.load(file).transpose(transpose)
        for i in [(x,y,z) for x in range(a.shape[0]) for y in range(a.shape[1]) \
                                                    for z in range(a.shape[2])]:
            a[i] = 0 if a[i] < 0.001 else 1
        ax.voxels(np.flip(a,2), facecolors=color, edgecolor='black')
        plt.savefig(savepth+"{}-3D-{}.jpg".format(path.basename(file).replace(".npy", ""), count))
        plt.close()
        count+=1

def makeGif(filelist, gifName):
    imgs = sorted(filelist, key = lambda x: int((x.split("-")[-1].replace(".jpg","")).replace("\n","")))
    imgs = [i.replace("\n","") for i in imgs]
    clip=mpy.ImageSequenceClip(imgs, fps=24)
    clip.write_gif(gifName, fps=24)

def sortbyname(files):
    return sorted([i for i in files], key=lambda x: \
                                    float((x.split("/")[-1]).split("-")[0].split("_")[0])*10 + \
                                    float((x.split("/")[-1]).split("-")[-1].replace(".npy", "")))
