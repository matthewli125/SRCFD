import h5py
import numpy as np
import matplotlib.pyplot as plt
import foamToPy

filepath = "gan_data.h5"

file = h5py.File(filepath)
lowres = file["lowres"]
highres = file["highres"]

randnum = np.random.randint(0, lowres.shape[0])

fig, axes = plt.subplots(nrows=3, ncols=5, figsize=(15,6))

axes[0][0].set_title("{} alpha".format(lowres[0][0].shape))
axes[0][1].set_title("{} p".format(lowres[0][0].shape))
axes[0][2].set_title("{} Ux".format(lowres[0][0].shape))
axes[0][3].set_title("{} Uy".format(lowres[0][0].shape))
axes[0][4].set_title("{} Uz".format(lowres[0][0].shape))

axes[1][0].set_title("{} alpha".format(highres[0][0].shape))
axes[1][1].set_title("{} p".format(highres[0][0].shape))
axes[1][2].set_title("{} Ux".format(highres[0][0].shape))
axes[1][3].set_title("{} Uy".format(highres[0][0].shape))
axes[1][4].set_title("{} Uz".format(highres[0][0].shape))

lowres_case = lowres[randnum]
highres_case = highres[randnum]


for i in range(5):
    axes[0][i].imshow(np.squeeze(lowres_case[i]))
    axes[1][i].imshow(np.squeeze(highres_case[i]))

axes[2][0].imshow(np.squeeze(foamToPy.buildarr((64,64,1), "D:/openfoamData/dambreak_cases4/1_highres/0.05/alpha.water", "D:/openfoamData/dambreak_cases4/1_highres/system/blockMeshDict")))
axes[2][1].imshow(np.squeeze(foamToPy.buildarr((64,64,1), "D:/openfoamData/dambreak_cases4/1_highres/0.05/p", "D:/openfoamData/dambreak_cases4/1_highres/system/blockMeshDict")))
axes[2][2].imshow(np.squeeze(foamToPy.buildarr((64,64,1), "D:/openfoamData/dambreak_cases4/1_highres/0.05/U", "D:/openfoamData/dambreak_cases4/1_highres/system/blockMeshDict", channel=0)))
axes[2][3].imshow(np.squeeze(foamToPy.buildarr((64,64,1), "D:/openfoamData/dambreak_cases4/1_highres/0.05/U", "D:/openfoamData/dambreak_cases4/1_highres/system/blockMeshDict",channel=1)))
axes[2][4].imshow(np.squeeze(foamToPy.buildarr((64,64,1), "D:/openfoamData/dambreak_cases4/1_highres/0.05/U", "D:/openfoamData/dambreak_cases4/1_highres/system/blockMeshDict", channel=2)))


plt.tight_layout()
plt.show()
