import subprocess
from os import listdir
from tqdm import tqdm
import numpy as np
import multiprocessing as mp

numCores = mp.cpu_count()
print(str(numCores) + "cores available for use\n")

num = 400
loc = "/mnt/d/openfoamData/dambreak_cases2"
partial = True

# calls the openFoam executable Allrun sequentially for a given list of
# directories
def Run(cases):
    failedCases = []
    for i in tqdm(cases):
        result1 = subprocess.call([loc + "/" + i + "/Allclean"])
        result2 = subprocess.call([loc + "/" + i + "/Allrun"])
        if result2 != 0:
            failedCases.append(i)

# finds all the folders that have incomplete or empty timesteps and puts them
# all in a list for easier handling
def GetIncomplete():
    sum = 0
    incomplete = []
    print("searching for incomplete cases")
    for i in tqdm(list(listdir(loc))):
        for j in listdir(loc+"/"+i):
            sum+=1
        if sum < 109:
            incomplete.append(i)
        sum = 0
    return incomplete


def Distribute(cases):
    nextLargest = len(cases)
    while nextLargest % numCores > 0:
        nextLargest-=1

    distributedCases = list(np.split(np.array(cases)[:nextLargest], numCores))
    distributedCases = [list(i) for i in distributedCases]

    for i in range(len(cases[nextLargest:])):
        distributedCases[i % numCores].append(cases[nextLargest:][i])

    return distributedCases

if __name__ == "__main__":
    incomplete = GetIncomplete()
    print(str(len(incomplete)) + "cases to be handled\n")
    pool = mp.Pool(numCores)
    pool.map(Run, Distribute(incomplete))
