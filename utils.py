import os
import shutil
import numpy as np
from tempfile import TemporaryFile
import matplotlib.pyplot as plt
from pathlib import Path
np.set_printoptions(threshold=np.inf)




def removelogs(res):
    if res == "high":
        current = 0
        for filename in os.listdir():
            for filename in os.listdir("DB{}_highres".format(current)):
                if (filename == "log.blockMesh") or (filename == "log.interFoam") or (filename == "log.setFields"):
                    try:
                        os.remove("DB{}_highres/".format(current) + filename)
                        print("DB{}_highres cleaned!".format(current))
                    except OSError:
                        pass
            if current < 399:
                current+=1
    elif res == "low":
        current = 0
        for filename in os.listdir():
            for filename in os.listdir("DB{}".format(current)):
                if (filename == "log.blockMesh") or (filename == "log.interFoam") or (filename == "log.setFields"):
                    try:
                        os.remove("DB{}/".format(current) + filename)
                        print("DB{} cleaned!".format(current))
                    except OSError:
                        pass
            if current < 399:
                current+=1
    
def copyfiles():
    file1 = "alpha.water.orig"
    file2 = "blockMeshDict"
    for i in range(400):
        shutil.copy(file1, "DB{}_highres/0".format(i))
        shutil.copyfile(file2, "DB{}_highres/system/blockMeshDict".format(i))

def allClean():
    for i in range(400):
        for filename in os.listdir("DB{}".format(i)):
            if (filename != "0") and (filename !="constant") and (filename != "system") and (filename != "Allclean") and (filename != "Allrun"):
                try:
                    shutil.rmtree("DB{}/{}".format(i, filename))
                except OSError:
                    pass
        try:
            shutil.rmtree("DB{}/constant/polyMesh".format(i))
        except OSError:
            pass
        print("case DB{} has been successfully cleaned".format(i))
    removelogs()


def countTimes():
    done = 0
    for i in range(400):
        count = 0
        for filename in os.listdir("DB{}_highres".format(i)):
            count+=1
        print("DB{}_highres has {} timesteps".format(i, count))
    for i in range(400):
        count = 0    
        for filename in os.listdir("DB{}".format(i)):
            count+=1
        if count !=109:
            print("DB{} has {} timesteps".format(i, count))
            done +=1
    print("{} are done cleaning.".format(done))

def checkComplete():
    i = 0
    for filename in os.listdir(os.getcwd()):
        if filename.find("DB{}".format(i)):
            print(filename)
        else:
            continue
        i+=1
    print("done")

def cleanup():
    incomplete = []
    out = ""
    for i in range(400):
        count= 0
        for filename in os.listdir("DB{}".format(i)):
            count+=1
        if count < 108:
            incomplete.append(i)
    for i in incomplete:
        out+="(rm DB{}/log.interFoam && cd DB{} && interFoam) & ".format(i, i)
    return out

def plotxyz(num, time, res = "high"):
    if res == "high":
        with open("DB0_highres/0/Cx", "r") as file:
            X = file.readlines()[23:1043]
            X = list(map(lambda x: float(x), X))
        file.close()
        with open("DB0_highres/0/Cy", "r") as file:
            Y = file.readlines()[23:1043]
            Y = list(map(lambda x: float(x), Y))
        file.close()
        with open("DB{}_highres/{}/alpha.water".format(num, time), "r") as file:
            Z = file.readlines()[23:1043]
            Z = list(map(lambda x: float(x)*400 + 1, Z))
        file.close()
    elif res == "low":
        with open("DB0/5/Cx", "r") as file:
            X = file.readlines()[23:278]
            X = list(map(lambda x: float(x), X))
        file.close()
        with open("DB0/5/Cy", "r") as file:
            Y = file.readlines()[23:278]
            Y = list(map(lambda x: float(x), Y))
        file.close()
        with open("DB{}/{}/alpha.water".format(num, time), "r") as file:
            Z = file.readlines()[23:278]
            Z = list(map(lambda x: float(x)*400 + 1, Z))
        file.close()

    plt.scatter(X, Y, Z)
    plt.show()

def plotxy(res = "high"):
    if res == "high":
        with open("DB0_highres/5/Cx",  "r") as file:
            X = file.readlines()[23:1043]
            X = list(map(lambda x: float(x), X))
        file.close()
        with open("DB0_highres/5/Cy", "r") as file:
            Y = file.readlines()[23:1043]
            Y = list(map(lambda x: float(x), Y))
        file.close()
    elif res == "low":
        with open("DB0/5/Cx", "r") as file:
            X = file.readlines()[23:278]
            X = list(map(lambda x: float(x), X))
        file.close()
        with open("DB0/5/Cy", "r") as file:
            Y = file.readlines()[23:278]
            Y = list(map(lambda x: float(x), Y))
        file.close()
        
    plt.scatter(X, Y)
    plt.show()

def saveallhighres():
    for i in range(0,400):
        try:
            savehighres(i, "alpha.water", False)
        except ValueError:
            pass
        try:
            savehighres(i, "p", False)
        except ValueError:
            pass
        try:
            savehighres(i, "p_rgh", False)
        except ValueError:
            pass
        
def saveallLowres():
    for i in range(0,400):
        try:
            savelowres(i, "alpha.water", False)
        except ValueError:
            pass
        try:
            savelowres(i, "p", False)
        except ValueError:
            pass
        try:
            savelowres(i, "p_rgh", False)
        except ValueError:
            pass
        
    
def savehighres(num, filename, plot):
    for j in range(5, 501, 5):
        array = np.zeros(shape = [32,32])
        if int(j/100) == j/100:
            a = int(j/100)
        else:
            a = j/100

        
        with open("DB{}_highres/{}/{}".format(num, a, filename), 'r') as file:
            water = file.readlines()[23:1043]
            water = list(map(lambda x: float(x), water))
            #print(water[0])
        file.close()


        for i in range(2):
            array[31-i][:16] = water[i*16: i*16+16]
        
        for i in range(2):
            array[31-i][18:] = water[i*14+32: i*14+14+32]

        for i in range(0,29):
            array[31-i-2][:16] = water[i*16+32+28 : i*16+16+32+28]

        for i in range(0,29):
            array[31-i-2][16:18] = water[i*2+32+28+30*16:i*2+2+ 32+28+30*16]

        for i in range(0,29):
            array[31-i-2][18:] = water[i*14+32+28+30*16+30*2:i*14+14+32+28+30*16+30*2]
        if plot == True:
            plt.imshow(array)
            plt.savefig("plots//highres{}_DB{}_highres_{}_{}.png".format(j,num, filename, a))
        #np.save("{}_highres/DB{}_highres_{}_@time = {}.npy".format(filename, num, filename, a), array)

def savelowres(num, filename, plot):
    for j in range(5, 501, 5):
        array = np.zeros(shape = [16,16])
        if int(j/100) == j/100:
            a = int(j/100)
        else:
            a = j/100

        if Path("{}_lowres/DB{}_{}_@time = {}.npy".format(filename, num, filename, a)).exists():
            print("{} {} {} already exists".format(filename, num, a))
            return
        
        with open("DB{}/{}/{}".format(num, a, filename), 'r') as file:
            water = file.readlines()[23:278]
            water = list(map(lambda x: float(x), water))
            #print(water[0])
        file.close()


        for i in range(1):
            array[15-i][:8] = water[i*8: i*8+8]
        
        for i in range(1):
            array[15-i][9:] = water[i*7+8: i*7+7+8]

        for i in range(0,14):
            array[15-i-1][:8] = water[i*8+8+7:i*8+8+8+7]

        for i in range(0,14):
            array[15-i-1][8] = water[i+8+7+15*8]

        for i in range(0,14):
            array[15-i-1][9:] = water[i*7+8+7+15*8+15: i*7+7+8+7+15*8+15]
        if plot == True:
            plt.imshow(array)
            plt.savefig("plots/lowres/{}_DB{}_{}_{}.png".format(j,num, filename, a))
        #np.save("{}_lowres/DB{}_{}_@time = {}.npy".format(filename, num, filename, a), array)
   
