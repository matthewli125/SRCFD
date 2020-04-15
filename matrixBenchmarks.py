from time import perf_counter
from timeit import timeit, Timer
from decimal import Decimal
from foamToPy import buildarr
from matrix import *
from tqdm import tqdm
from functools import partial

def timeFunc(func, *args, **kwargs):
    # start = Decimal(perf_counter())
    t = Timer(partial(func, *args, **kwargs))
    retVal = t.timeit(number=100)
    # end = Decimal(perf_counter())
    # return end-start
    return retVal


if __name__ == "__main__":
    a = np.squeeze(buildarr((512,512,1), "D:/openfoamData/dambreak_cases5/1_highres/2./alpha.water","D:/openfoamData/dambreak_cases5/0_highres/system/blockMeshDict"))

    seqTimes = {"min":0, "max":0, "avg":0, "normalize":0}
    parTimes = {"min":0, "max":0, "avg":0, "normalize":0}

    ##initialize jit functions
    pmatrixMin(a)
    pmatrixMax(a)
    pmatrixAvg(a)
    pmatrixNormalize(a, pmatrixMin(a), pmatrixMax(a))

    seqTimes["min"] += timeFunc(matrixMin, a)
    seqTimes["max"] += timeFunc(matrixMax, a)
    seqTimes["avg"] += timeFunc(matrixAvg, a)
    seqTimes["normalize"] += timeFunc(matrixNormalize, a, matrixMin(a), matrixMax(a))

    parTimes["min"] += timeFunc(pmatrixMin, a)
    parTimes["max"] += timeFunc(pmatrixMax, a)
    parTimes["avg"] += timeFunc(pmatrixAvg, a)
    parTimes["normalize"] += timeFunc(pmatrixNormalize, a, pmatrixMin(a), pmatrixMax(a))

    print("parallel matrix min:", "{0:1.2f}X improvement".format(seqTimes["min"]/parTimes["min"]))
    print("parallel matrix max:", "{0:1.2f}X improvement".format(seqTimes["max"]/parTimes["max"]))
    print("parallel matrix average:", "{0:1.2f}X improvement".format(seqTimes["avg"]/parTimes["avg"]))
    print("parallel matrix normalize:", "{0:1.2f}X improvement".format(seqTimes["normalize"]/parTimes["normalize"]))
