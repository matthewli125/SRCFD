import re
from os import system
from random import uniform
from decimal import Decimal
from shutil import copytree



lowrespath = r"C:\Users\Matthew Li\AppData\Local\Packages\CanonicalGroupLimited.UbuntuonWindows_79rhkp1fndgsc\LocalState\rootfs\home\matthewli125\OpenFOAM\OpenFOAM-v1812\tutorials\multiphase\interFoam\laminar\damBreak\\damBreak"
lowresdst = "D:\\openfoamData\\dambreak_cases\\DB{}"
highrespath = "C:\\Users\\Matthew Li\\AppData\\Local\\Packages\\CanonicalGroupLimited.UbuntuonWindows_79rhkp1fndgsc\\LocalState\\rootfs\\home\\matthewli125\\OpenFOAM\\matthewli125-v1812\\run\\dambreakhighres\\damBreak"
highresdst = "D:\\openfoamData\\dambreak_cases\\DB{}_highres"



def blockmeshdict():
    for i in range(400):
        with open(highresdst.format(i) + "\\system\\blockMeshDict", 'r') as file:
            blockMeshDict = file.readlines()

        blockMeshDict[51] = "    hex (5 6 10 9 17 18 22 21) (2 30 1) simpleGrading (1 2 1)"
        

        with open(highresdst.format(i) + "\\system\\blockMeshDict", 'w') as file:
            file.writelines(blockMeshDict)
        #a = input("pause")


def randomproperties():
    for i in range(400):
        

        copytree(lowrespath, lowresdst.format(i))
        copytree(highrespath, highresdst.format(i))


        waterheight = round(Decimal(uniform(0, 0.584)), 5)
        waterwidth =  round(Decimal(uniform(0, 0.584)), 5)
        gnew = round(Decimal(uniform(50, 0)), 5)
        nunew = round(Decimal(uniform(0.0000001, 1)), 5)
        rhonew = round(Decimal(uniform(0,100000)), 5)
        sigmanew = round(Decimal(uniform(0,10)), 5)
        
        


        #low res
        with open(lowresdst.format(i) + "\\system\\setFieldsDict", 'r') as file:
            setFieldsDict = file.readlines()
        waterSize = setFieldsDict[26]
        waterSize = re.findall(r'[0-9.]+|\D',waterSize)

        waterSize[22] = waterwidth
        waterSize[24] = waterheight

        setFieldsDict[26] = "".join(map(str, waterSize))

        with open(lowresdst.format(i) + "\\system\\setFieldsDict", 'w') as file:
            file.writelines(setFieldsDict)


        with open(lowresdst.format(i) + "\\constant\\g", 'r') as file:
            gDict = file.readlines()
        g = gDict[18]
        g = re.findall(r'[0-9.]+|\D',g)
        g[20] = gnew

        gDict[18] = "".join(map(str,g))

        with open(lowresdst.format(i) + "\\constant\\g", "w") as file:
            file.writelines(gDict)


        with open(lowresdst.format(i) + "\\constant\\transportProperties", "r") as file:
            transDict = file.readlines()
            
        nu = transDict[22]
        nu = re.findall(r'[0-9.]+|\D', nu)
        nu[20] = nunew
        transDict[22] = "".join(map(str, nu))

        rho = transDict[23]
        rho = re.findall(r'[0-9.]+|\D', rho)
        rho[20] = rhonew
        transDict[23] = "".join(map(str, rho))

        sigma = transDict[33]
        sigma = re.findall(r'[0-9.]+|\D', sigma)
        sigma[17] = sigmanew
        transDict[33] = "".join(map(str, sigma))

        with open(lowresdst.format(i) + "\\constant\\transportProperties", "w") as file:
            file.writelines(transDict)



        #high res
        with open(highresdst.format(i) + "\\system\\setFieldsDict", 'r') as file:
            setFieldsDict = file.readlines()
        waterSize = setFieldsDict[26]
        waterSize = re.findall(r'[0-9.]+|\D',waterSize)

        waterSize[22] = waterwidth
        waterSize[24] = waterheight

        setFieldsDict[26] = "".join(map(str, waterSize))

        with open(highresdst.format(i) + "\\system\\setFieldsDict", 'w') as file:
            file.writelines(setFieldsDict)


        with open(highresdst.format(i) + "\\constant\\g", 'r') as file:
            gDict = file.readlines()
        g = gDict[18]
        g = re.findall(r'[0-9.]+|\D',g)
        g[20] = gnew

        gDict[18] = "".join(map(str,g))

        with open(highresdst.format(i) + "\\constant\\g", "w") as file:
            file.writelines(gDict)


        with open(highresdst.format(i) + "\\constant\\transportProperties", "r") as file:
            transDict = file.readlines()
            
        nu = transDict[22]
        nu = re.findall(r'[0-9.]+|\D', nu)
        nu[20] = nunew
        transDict[22] = "".join(map(str, nu))

        rho = transDict[23]
        rho = re.findall(r'[0-9.]+|\D', rho)
        rho[20] = rhonew
        transDict[23] = "".join(map(str, rho))

        sigma = transDict[33]
        sigma = re.findall(r'[0-9.]+|\D', sigma)
        sigma[17] = sigmanew
        transDict[33] = "".join(map(str, sigma))

        with open(highresdst.format(i) + "\\constant\\transportProperties", "w") as file:
            file.writelines(transDict)

