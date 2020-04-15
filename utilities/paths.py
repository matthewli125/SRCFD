from os import listdir
from sys import platform

if platform == "win32":

    PTH = "D:\\openfoamData\\dambreak_cases5"
    DATAPTH = "D:\\openfoamData\\newcodedata5"
    blockMeshDictPath = "\\system\\blockMeshDict"
    setFieldsDictPath = "\\system\\setFieldsDict"
    lowResPath = "D:\\openfoamData\\damBreak_lowres"
    highResPath = "D:\\openfoamData\\damBreak_highres"
    FILES = ["alpha.water","p", "p_rgh"]

    PTHd = listdir(PTH)
    HRSAVEPTH = PTH + "\\highres\\"
    LRSAVEPTH = PTH + "\\lowres\\"
    HRDATAPTH = DATAPTH + "\\highres\\"
    LRDATAPTH = DATAPTH + "\\lowres\\"
    lowResDST = PTH + "\\{}"
    highResDST = PTH + "\\{}_highres"

    # HRSAVEPTH = "D:\\openfoamData\\newcodedata3\\highres\\"
    # LRSAVEPTH = "D:\\openfoamData\\newcodedata3\\lowres\\"
    # lowResDST = "D:\\openfoamData\\dambreak_cases2\\{}"
    # highResDST = "D:\\openfoamData\\dambreak_cases2\\{}_highres"

elif platform == "linux" or platform == "linux2":

    PTH = "/mnt/d/openfoamData/dambreak_cases5"
    DATAPTH = "mnt/d/openfoamData/newcodedata5"
    blockMeshDictPath = "/system/blockMeshDict"
    setFieldsDictPath = "/system/setFieldsDict"
    lowResPath = "/mnt/d/openfoamData/damBreak_lowres"
    highResPath = "/mnt/d/openfoamData/damBreak_highres"
    FILES = ["alpha.water","p", "p_rgh"]


    PTHd = listdir(PTH)
    HRSAVEPTH = PTH + "/highres/"
    LRSAVEPTH = PTH + "/lowres/"
    HRDATAPTH = DATAPTH + "/highres/"
    LRDATAPTH = DATAPTH + "/lowres/"
    lowResDST = PTH + "/{}"
    highResDST = PTH + "/{}_highres"


    # HRSAVEPTH = "/mnt/d/openfoamData/newcodedata3/highres/"
    # LRSAVEPTH = "/mnt/d/openfoamData/newcodedata3/lowres/"
    # lowResDST = "/mnt/d/openfoamData/dambreak_cases2/{}"
    # highResDST = "/mnt/d/openfoamData/dambreak_cases2/{}_highres"
