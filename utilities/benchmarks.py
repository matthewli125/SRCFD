from random import randint
from timeit import timeit
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from keras import backend as K
# from keras.models import load_model
# import h5py
import cv2
from math import floor

numRuns = 100

# data = h5py.File("alpha.waternew.h5", "r")
# lowres = [data["lowres"][i] for i in range(55, 6110, 61)]
# highres = [data["highres"][i] for i in range(55, 6110, 61)]

lowres = np.array([np.load("D:/openfoamData/newcodedata5/lowres/0-256x256x1-alpha.water-2.95.npy")])
highres = np.array([np.load("D:/openfoamData/newcodedata5/highres/0_highres-512x512x1-alpha.water-2.95.npy")])

def PSNR(y_true, y_pred):
	max_pixel = 1.0
	return 10.0 * tf_log10((max_pixel ** 2) / (K.mean(K.square(y_pred - y_true))))

def tf_log10(x):
  numerator = tf.math.log(x)
  denominator = tf.math.log(tf.constant(10, dtype=numerator.dtype))
  return numerator / denominator

# benchmarking function using the timeit module, gets the average running time
# of a function, with the number of runs set by numRuns
def time(func):
    exTime = timeit(func, number=numRuns, globals=globals())/numRuns*1000000
    # print("{} executed {} times with average time of {} μs". \
    #                             format(func.split("(")[0], numRuns, round(exTime,4)))
    return exTime




def nearest_upsample(arr, n):
    return cv2.resize(arr, dsize=(arr.shape[0]*n, arr.shape[1]*n), interpolation = cv2.INTER_NEAREST)

def linear_upsample(arr, n):
    return cv2.resize(arr, dsize=(arr.shape[0]*n, arr.shape[1]*n), interpolation = cv2.INTER_LINEAR)

def bicubic_upsample(arr, n):
    return cv2.resize(arr, dsize=(arr.shape[0]*n, arr.shape[1]*n), interpolation = cv2.INTER_CUBIC)

def lanczos_upsample(arr, n):
    return cv2.resize(arr, dsize=(arr.shape[0]*n, arr.shape[1]*n), interpolation = cv2.INTER_LANCZOS4)

# model = "D:/projects/SRCFD/neural_net/fsrcnn_model-Wed_Mar_11_03-14-07_2020.h5"
# neural_net = load_model(model, custom_objects = {'PSNR' : PSNR})
#
# def NN_predict(arr):
#     img = np.squeeze(neural_net.predict(arr.reshape(1,32,32,1), verbose = 0))
#     for i in range(len(img)):
#         for j in range(len(img)):
#             if img[i][j] < 0.001:
#                 img[i][j] = 0
#     return img


# times = {"nearest_neighbor":0, "linear":0, "bicubic":0, "lanczos":0, "neural_net":0}
# results = {"nearest_neighbor":[], "linear":[], "bicubic":[], "lanczos":[], "neural_net":[]}

times = {"nearest_neighbor":0, "linear":0, "bicubic":0, "lanczos":0}
results = {"nearest_neighbor":[], "linear":[], "bicubic":[], "lanczos":[]}

for i in range(len(lowres)):
    times["nearest_neighbor"]+=time("nearest_upsample(lowres[{}],2)".format(i))
    times["linear"]+=time("linear_upsample(lowres[{}],2)".format(i))
    times["bicubic"]+=time("bicubic_upsample(lowres[{}],2)".format(i))
    times["lanczos"]+=time("lanczos_upsample(lowres[{}],2)".format(i))
    # times["neural_net"]+=time("NN_predict(lowres[{}])".format(i))

for i in range(len(lowres)):
    results["nearest_neighbor"].append(nearest_upsample(lowres[i],2))
    results["linear"].append(linear_upsample(lowres[i],2))
    results["bicubic"].append(bicubic_upsample(lowres[i],2))
    results["lanczos"].append(lanczos_upsample(lowres[i],2))
    # results["neural_net"].append(NN_predict(lowres[i]))
#     fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(8,8))
#     axes[0][0].imshow(np.squeeze(lowres[i]))
#     axes[0][1].imshow(np.squeeze(highres[i]))
#     axes[0][2].imshow(np.squeeze(results["neural_net"][i]))
#     axes[1][0].imshow(np.squeeze(results["linear"][i]))
#     axes[1][1].imshow(np.squeeze(results["bicubic"][i]))
#     axes[1][2].imshow(np.squeeze(results["lanczos"][i]))
#     plt.savefig("comparison/{}.jpeg".format(i))
#     plt.close()

for i in times:
    times[i] = times[i]/len(lowres)
print(times)

for i in results:
    results[i] = sum([PSNR(np.squeeze(highres[j]),results[i][j]).numpy() for j in range(len(results[i]))])/len(results[i])
print(results)

fig, axes = plt.subplots(nrows = 1, ncols = 4, figsize = (32,8))
axes[0].imshow(np.squeeze(lowres[0]))
axes[1].imshow(np.squeeze(linear_upsample(lowres[0], 2)))
axes[2].imshow(np.squeeze(highres[0]))
axes[3].imshow(np.squeeze(linear_upsample(highres[0],2)))

plt.show()
