import numpy as np
from numba import jit, prange, njit
from timer import timeit_wrapper
from functools import lru_cache

##SEQUENTIAL

def matrixMax(arr): # finds max value of a 2d matrix
    return np.max([np.max(i) for i in arr])

def matrixMin(arr): # finds min value of a 2d matrix
    return np.min([np.min(i) for i in arr])

def matrixAvg(arr): # finds average value of a 2d matrix
    return np.mean([np.mean(i) for i in arr])

def matrixNormalize(arr, min, max): # normalizes values of a 2d matrix to 0 and 1
    return [(i - min)/(max - min) for i in arr]


##PARALLEL

def pmatrixMax(arr):
    prowMaxs(arr)
    return np.max(arr)

@njit(parallel=True)
def prowMaxs(arr):
    for i in prange(len(arr)):
        arr[i] = np.max(arr[i])

def pmatrixMin(arr):
    prowMins(arr)
    return np.min(arr)

@njit(parallel=True)
def prowMins(arr):
    for i in prange(len(arr)):
        arr[i] = np.min(arr[i])

def pmatrixAvg(arr):
    prowMeans(arr)
    return np.mean(arr)

@njit(parallel=True)
def prowMeans(arr):
    for i in prange(len(arr)):
        arr[i] = np.mean(arr[i])

@njit(parallel=True)
def pmatrixNormalize(arr, min, max):
    for i in prange(len(arr)):
        for j in prange(len(arr)):
            arr[i,j] = (arr[i][j] - min)/(max - min)
