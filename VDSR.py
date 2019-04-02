##import os
##os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

from keras.layers import Input, Conv2D, Concatenate, Conv2DTranspose
from keras.models import Model
from keras.models import Sequential
from keras.optimizers import Adam
import numpy as np
from os import listdir
import h5py

##from keras import backend as K
##K.set_image_dim_ordering('th')

SHAPE = (16,16,1)
input_dir = "D:/openfoamData/alpha.water_lowres_small"
label_dir = "D:/openfoamData/alpha.water_highres_small"


model = Sequential()
model.add(Conv2D(64, (9,9), activation='relu', input_shape=(32, 32, 1), name = "first_layer"))
model.add(Conv2D(32, (1,1), activation='relu', name = "middle_layer"))
model.add(Conv2D(1, (5,5), activation='relu', name = "middle_layer1"))
model.add(Conv2DTranspose(1, (13, 13), activation = 'relu'))
adam = Adam(lr=0.0003)
model.compile(optimizer=adam, loss='mean_squared_error', metrics=['mean_squared_error'])

print(model.summary())
temp = 0
data = h5py.File("D:/openfoamData/dambreak_cases/water_large.h5", "r")
X = data["lowres"][:]
y = data["highres"][:]



model.fit(x=X, y = y, batch_size = 128, epochs = 1, verbose = 1)
#m.fit(x = X, y = y, batch_size = 32, epochs = 10)
##while True:
##    model.fit(X, y, batch_size=128, nb_epoch=5)
##    if args.save:
##        print("Saving model " + str(count * 5))
##        model.save(join(args.save, 'model_' + str(count * 5) + '.h5'))
##    count += 1

