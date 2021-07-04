from os import listdir
import subprocess
from multiprocessing import cpu_count
import matplotlib.pyplot as plt

def run_process(dir):
    cwd = "".join("/",dir)
    subprocess.run("blockMesh > blockMesh.log", cwd=cwd)
    subprocess.run("setFields > setFields.log", cwd=cwd)
    subprocess.run("decomposePar > decomposePar.log", cwd=cwd)
    #subprocess.run("interFoam > interFoam.log", cwd=cwd)
    subprocess.run("reconstructPar > reconstructPar.log", cwd=cwd)
    print(dir+" done!")


num_cores = cpu_count()
print(str(num_cores)+" cores available for use")
