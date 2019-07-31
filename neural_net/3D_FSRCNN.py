from keras.layers import Input,Conv2D,Conv2DTranspose,Conv3D,Conv3DTranspose,Concatenate
from keras.models import Model
from keras.layers.advanced_activations import PReLU
from keras import backend as K
import tensorflow as tf
from keras.models import Sequential
from keras.optimizers import Adam
from keras.models import load_model
import numpy as np
from os import listdir
import os
import h5py
import cv2
import time

# put path to h5 file here
data_pth = ""

def PSNR(y_true,y_pred):
	max_pixel = 1.0
	return 10.0 * tf_log10((max_pixel ** 2) / (K.mean(K.square(y_pred - y_true))))

def tf_log10(x):
  numerator = tf.math.log(x)
  denominator = tf.math.log(tf.constant(10,dtype=numerator.dtype))
  return numerator / denominator


input_img = Input(shape=(16,16,16,1))

model = Conv3D(31,(2,2,2),padding='same',kernel_initializer='he_normal')(input_img)
model = PReLU()(model)

model = Conv3D(16,(1,1,1),padding='same',kernel_initializer='he_normal')(model)
model = PReLU()(model)

model = Conv3D(12,(3,3,3),padding='same',kernel_initializer='he_normal')(model)
model = PReLU()(model)
model = Conv3D(12,(3,3,3),padding='same',kernel_initializer='he_normal')(model)
model = PReLU()(model)


model = Conv3D(25,(1,1,1),padding='same',kernel_initializer='he_normal')(model)
model = PReLU()(model)

model = Conv3DTranspose(1,(2,2,2),strides=(2,2,1),padding='same')(model)

output_img = model

model = Model(input_img,output_img)
yadam = Adam(lr = 0.01)
model.compile(optimizer=yadam,loss='mse',metrics=[PSNR,'accuracy'])


print(model.summary())

def normalize(X):
    X_min = X.min(axis=(1,2),keepdims = True)
    X_max = X.max(axis = (1,2),keepdims = True)
    return (X-X_min)/(X_max-X_min)



data = h5py.File(data_pth,"r")
X = data["lowres"][10000:]
X_normal = normalize(X)
y = data["highres"][10000:]
y_normal = normalize(y)

X_test = data["lowres"][48:10000]
X_test_normal = normalize(X_test)

y_test = data["highres"][48:10000]
y_test_normal = normalize(y_test)

print(X.shape)
print(y.shape)

train_time = ((time.asctime().replace("  "," ")).replace(" ","_")).replace(":","-")
H = model.fit(x=X,y=y,batch_size = 128,validation_data=(X_test,y_test),epochs=200,verbose=1)

model.save("fsrcnn_model-3d-{}.h5".format(train_time))
score = model.evaluate(X_test,y_test,verbose=1)
print('Test loss:',score[0])
print('Test accuracy:',score[1])
