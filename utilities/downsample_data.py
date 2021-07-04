import numpy as np
import cv2
from os import listdir
from tqdm import tqdm

highres_path = "E:/gan_data/highres/"
lowres_path = "E:/gan_data/lowres_downsample/"

count = 0

def unfold(arr):
    global count
    for i in arr:
        np.save("E:/gan_data/highres_single/%s.npy" % count, i)
        count+=1

def downsample(arr):
    return np.array(cv2.resize(arr, (16,16), interpolation=cv2.INTER_LINEAR))


if __name__ == "__main__":
    # for i in tqdm(listdir(highres_path)):
    #     hr = np.load(highres_path + i)
    #     unfold(hr)
    pth = "E:/gan_data/highres_single/"

    for i in tqdm(listdir(pth)):
        hr = np.load(pth + i)
        slices = np.split(hr, 5, axis=-1)
        downsampled_slices = [downsample(i) for i in slices]
        downsampled = np.stack(downsampled_slices, axis=-1)
        np.save(lowres_path + i, downsampled)

    # hr = listdir("E:/gan_data/highres_single")
    # lr = listdir("E:/gan_data/lowres_downsample")
    #
    #
    # import matplotlib.pyplot as plt
    #
    # for i in [i for i in hr if i in lr]:
    #     fig, ax = plt.subplots(nrows=1,ncols=2,figsize=(10,5))
    #     ax[0].imshow(np.squeeze(np.split(np.load(lowres_path + i), 5, axis=-1)[0]))
    #     ax[1].imshow(np.squeeze(np.split(np.load("E:/gan_data/highres_single/" + i),5,axis=-1)[0]))
    #     plt.show()
