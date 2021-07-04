import numpy as np
import os
from foamToPy import buildarr

class Foam_Case:
    def __init__(self, res, file_path, type):
        self.type = type #highres or lowres
        self.res = res
        self.mesh_file = os.path.dirname(file_path) + "/system/blockMeshDict"
        self.alpha_path = file_path + "/alpha.water"
        self.U_path = file_path + "/U"
        self.p_path = file_path + "/p"

    def fetch(self):
        self.alpha = np.squeeze(buildarr(self.res, self.alpha_path, self.mesh_file))
        self.p     = np.squeeze(buildarr(self.res, self.p_path, self.mesh_file))
        self.Ux    = np.squeeze(buildarr(self.res, self.U_path, self.mesh_file, channel = 0))
        self.Uy    = np.squeeze(buildarr(self.res, self.U_path, self.mesh_file, channel = 1))
        self.Uz    = np.squeeze(buildarr(self.res, self.U_path, self.mesh_file, channel = 2))

        return self

    def crunch(self):
        del self.alpha
        del self.p
        del self.Ux
        del self.Uy
        del self.Uz

    def enum(self):
        return np.stack([self.alpha, self.p, self.Ux, self.Uy, self.Uz], axis=-1)


# for debugging purposes, run with python3 -i; run with linux
if __name__ == "__main__":
    # mesh_file = "/mnt/d/openfoamData/dambreak_cases4/6_highres/system/blockMeshDict"
    file_path = "/mnt/d/openfoamData/dambreak_cases4/772_highres/1.15"

    sample = Foam_Case((64,64,1), file_path, "test")
