from keras.models import load_model
import h5py
import numpy as np
import matplotlib.pyplot as plt
import cv2
from keras.optimizers import Adam
import os
from keras import backend as K
import tensorflow as tf

def PSNR(y_true, y_pred):
	max_pixel = 1.0
	return 10.0 * tf_log10((max_pixel ** 2) / (K.mean(K.square(y_pred - y_true))))

def tf_log10(x):
  numerator = tf.log(x)
  denominator = tf.log(tf.constant(10, dtype=numerator.dtype))
  return numerator / denominator


data = h5py.File("D:/water_large_sorted.h5")
x = data["lowres"][:48]
##x2 = []
##x = np.squeeze(x)
##for i in range(len(x)):
##    temp = cv2.resize(x[i], (16, 16), interpolation = cv2.INTER_CUBIC)
##    temp = temp.reshape(16, 16, 1)
##    x2.append(temp)
##x2 = np.asarray(x2)

modelname = input()

model = load_model(modelname, custom_objects = {'PSNR' : PSNR})

result = model.predict(x, verbose = 1)
result = result.reshape(48, 32, 32)

y = data["highres"][:48]
y = y.reshape(48, 32, 32)
for i in range(48):
    plt.imshow(y[i])
    plt.savefig("D:/SRCFD/truth/truth_fsrcnn {}.png".format(i))

for i in range(48):
    plt.imshow(result[i])
    plt.savefig("D:/SRCFD/neuralnetoutput/neural net output_fsrcnn {}.png".format(i))



import glob
import moviepy.editor as mpy
import time

time = ((time.asctime().replace("  ", " ")).replace(" ", "_")).replace(":", "-")

file_list = glob.glob('D:/SRCFD/neuralnetoutput/*.png')
list.sort(file_list, key=lambda x: int(x.split(' ')[3].split('.png')[0]))
print(file_list)
clip = mpy.ImageSequenceClip(file_list, fps=24)
clip.write_gif('neuralnet_fsrcnn {}.gif'.format(time), fps=24)

file_list = glob.glob('D:/SRCFD/truth/*.png')
list.sort(file_list, key=lambda x: int(x.split(' ')[1].split('.png')[0]))
print(file_list)
clip = mpy.ImageSequenceClip(file_list, fps=24)
clip.write_gif('truth_fsrcnn.gif'.format(time), fps=24)
