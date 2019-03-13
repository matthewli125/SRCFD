from keras.layers import Input, Conv2D, Concatenate
from keras.models import Model
from keras.optimizers import Adam

SHAPE = (1,2,3)

inputs = Input(shape = SHAPE)

outputs = Conv2D(64, (3,3), padding = "same", activation = "relu")(inputs)
outputs = Conv2D(64, (3,3), padding = "same", activation = "relu")(outputs)
outputs = Conv2D(64, (3,3), padding = "same", activation = "relu")(outputs)
outputs = Conv2D(64, (3,3), padding = "same", activation = "relu")(outputs)
outputs = Conv2D(64, (3,3), padding = "same", activation = "relu")(outputs)
outputs = Conv2D(64, (3,3), padding = "same", activation = "relu")(outputs)
outputs = Conv2D(64, (3,3), padding = "same", activation = "relu")(outputs)
outputs = Conv2D(64, (3,3), padding = "same", activation = "relu")(outputs)
outputs = Conv2D(64, (3,3), padding = "same", activation = "relu")(outputs)
outputs = Conv2D(64, (3,3), padding = "same", activation = "relu")(outputs)
outputs = Conv2D(64, (3,3), padding = "same", activation = "relu")(outputs)
outputs = Conv2D(64, (3,3), padding = "same", activation = "relu")(outputs)
outputs = Conv2D(64, (3,3), padding = "same", activation = "relu")(outputs)
outputs = Conv2D(64, (3,3), padding = "same", activation = "relu")(outputs)
outputs = Conv2D(64, (3,3), padding = "same", activation = "relu")(outputs)
outputs = Conv2D(64, (3,3), padding = "same", activation = "relu")(outputs)
outputs = Conv2D(64, (3,3), padding = "same", activation = "relu")(outputs)
outputs = Conv2D(64, (3,3), padding = "same", activation = "relu")(outputs)
outputs = Conv2D(64, (3,3), padding = "same", activation = "relu")(outputs)
outputs = Conv2D(64, (1,1), padding = "same", activation = "relu")(outputs)

output = Concatenate([inputs, outputs])
model = Model(inputs, outputs)
model.compile(Adam(lr = 0.1), "mse")
