from keras.layers import Input, Conv2D, Concatenate, Dense
from keras.models import Model
from keras.models import Sequential
from keras.optimizers import Adam
import numpy as np
from os import listdir

##from keras import backend as K
##K.set_image_dim_ordering('th')

SHAPE = (16,16,1)
input_dir = "D:/openfoamData/alpha.water_lowres"
label_dir = "alpha.water_highres"


model = Sequential()
model.add(Conv2D(64, (9,9), activation='relu', input_shape=(16, 16, 1), name = "first_layer"))
model.add(Conv2D(43, (1,1), activation='relu', name = "middle_layer"))
model.add(Conv2D(1, (5,5), activation='relu', name = "final_layer"))
adam = Adam(lr=0.0003)
model.compile(optimizer=adam, loss='mean_squared_error', metrics=['mean_squared_error'])

print(model.summary())
temp = 0
X = []
y = []

for file in listdir(input_dir):
    #print("ay")
    temp= np.load("alpha.water_lowres/" + file)
    temp = temp.reshape(16, 16, 1)
    X.append(temp)

for file in listdir(label_dir):
    #print("yuh")
    temp= np.load("alpha.water_highres/" + file)
    temp = temp.reshape(32, 32, 1)
    y.append(temp)

X = np.asarray(X)
y = np.asarray(y)


model.fit(x=X, y = y, batch_size = 32, epochs = 10, verbose = 1)
#m.fit(x = X, y = y, batch_size = 32, epochs = 10)
##while True:
##    model.fit(X, y, batch_size=128, nb_epoch=5)
##    if args.save:
##        print("Saving model " + str(count * 5))
##        model.save(join(args.save, 'model_' + str(count * 5) + '.h5'))
##    count += 1

