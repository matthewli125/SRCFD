from random import randint
from timeit import timeit
import numpy as np
import matplotlib.pyplot as plt
import cv2

numRuns = 1000

# benchmarking function using the timeit module, gets the average running time
# of a function, with the number of runs set by numRuns
def time(func):
    exTime = timeit(func, number=numRuns, globals=globals())/numRuns*1000000
    print("{} executed {} times with average time of {} μs". \
                                format(func.split("(")[0], numRuns, round(exTime,4)))

# test method for debugging; sorts a large list of numbers
def randsort():
    rand = [randint(0, 100000) for i in range(999999)]
    return sorted(rand)

def stupid_upsample(arr, n):
    final = np.zeros((n*arr.shape[0],n*arr.shape[1]))
    for i,j in np.ndindex(arr.shape):
        final[n*i:n*i+n,n*j:n*j+n] = np.full((n,n),arr[i][j])
    return final

def nearest_upsample(arr, n):
    return cv2.resize(arr, dsize=(arr.shape[0]*n, arr.shape[1]*n), interpolation = cv2.INTER_NEAREST)

def linear_upsample(arr, n):
    return cv2.resize(arr, dsize=(arr.shape[0]*n, arr.shape[1]*n))

def bicubic_upsample(arr, n):
    return cv2.resize(arr, dsize=(arr.shape[0]*n, arr.shape[1]*n), interpolation = cv2.INTER_CUBIC)


a = np.squeeze(np.load(r"/home/matthew/projects/SRCFD/overtime_data/0_highres-32x32x1-alphawater-0.1.npy"))

time("stupid_upsample(a,2)")
time("nearest_upsample(a,2)")
time("linear_upsample(a,2)")
time("bicubic_upsample(a,2)")
