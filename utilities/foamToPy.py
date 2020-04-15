import numpy as np
import re


#gets the vertices from the blockMeshDict file and makes a list of tuples, the
#list index of each vertex will correspond to its vertex number
def getVertices(File):
    points = []
    line = ""
    while line != "vertices\n":
        line = File.readline()
    line = File.readline()
    while line != ");\n":
        line = File.readline()
        if len(line)>4: points.append(eval(line[4:].replace(" ", ",")))
    return points


#gets the blocks from the blockMeshDict file, creates a list of blocks, which
#are sets of numbers corresponding to vertices
def getBlocks(File, points):
    # blocks = np.array([])
    blocks = []
    line = ""
    while line != "blocks\n":
        line = File.readline()
    line= File.readline()
    while line != ");\n":
        line = File.readline()
        filtered = re.split('\(|\)', line[4:])
        if len(filtered)<4: break
        Vertices = eval("[" + filtered[1].replace(" ", ",") + "]")
        Vertices = list(map(lambda x: points[x], Vertices))
        Density = eval("[" + filtered[3].replace(" ", ",") + "]")
        # blocks = np.append(blocks, (Vertices, Density))
        blocks.append((Vertices, Density))
    return blocks


#gets the largest xyz values from all vertices
def xyzmax(pointList):
    x = max(pointList, key = lambda x: x[0])[0]
    y = max(pointList, key = lambda x: x[1])[1]
    z = max(pointList, key = lambda x: x[2])[2]
    return [x,y,z]


#builds a block from data points in a file
def buildBlock(block, File):
    finalblock = np.empty(block[1])
    finalblock = finalblock.reshape(block[1][1], block[1][0], block[1][2])
    for k in range(block[1][2]):
        for i in reversed(range(block[1][1])):
            for j in range(block[1][0]):
                data = File.readline()
                if data[0] == "(":
                    points = [float(i) for i in data[1:-2].split(" ")]
                    point = points[0]
                else:
                    point = float(data)
                # finalblock[i][j][k] = point if point > 0.00001 else 0
                finalblock[i][j][k] = point
    return finalblock


#builds all the blocks in a given case into a single array, works for both 2d
#and 3d cases; does array arithmetic based on xyzmax and res (point density)
def buildarr(res, datafile, meshfile):
    final = np.zeros(res)
    data = open(datafile, "r")
    mesh = open(meshfile, "r")
    points = getVertices(mesh)
    XYZmax = np.array(xyzmax(points))
    mul = list(map(int, np.divide(res, XYZmax)))
    blocks = getBlocks(mesh, points)
    for i in range(23):
        discard = data.readline()
    for i in range(len(blocks)):
        st = blocks[i][0][0]
        st = (st[1]*mul[1], st[0]*mul[0], st[2]*mul[2])
        st = list(map(int, st))
        blocks[i] = buildBlock(blocks[i], data)
        shp = blocks[i].shape
        final[res[0]-(st[0]+shp[0]):res[0]-st[0], st[1]:st[1]+shp[1], \
                                          st[2]:st[2]+shp[2]] = blocks[i]
    return final


#performs buildarr on all cases in a directory, but sorts each level based on
#filename so they are saved and named in the correct time and case order. Uses
#global path vars. Set high to true if doing highres to follow file naming
#convention.
def buildall(res, high, savepth):
    FILES = ["alpha.water"]
    filFunc = lambda x: "highres" in x if high else "highres" not in x
    for i in sorted(filter(filFunc, PTHd), key= lambda x: int(x.split("_")[0])):
    # for i in [h + "_highres" for h in brokencases]:
        print("doing case {} {}\n".format(i, "highres" if high else "lowres"))
        for j in tqdm(list(filter(lambda x:x[0].isdigit(),listdir(PTH+"/"+i)))):
            for k in filter(lambda x: x in FILES, listdir(PTH+"/"+i+"/"+j)):
                try:
                    arr = buildarr(res, PTH+"/"+i+"/"+j+"/"+k, PTH+"/"+i+blockMeshDictPath)
                    np.save(savepth+"{}-{}x{}x{}-{}-{}.npy".format \
                                                        (i, *res, k, j), arr)
                except:
                    print("fail")


if __name__ == "__main__":
    buildall((256,256,1), False, LRDATAPTH)
    buildall((512,512,1), True, HRDATAPTH)
