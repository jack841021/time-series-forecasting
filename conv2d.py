import numpy
import random
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D
#%%
x, y = numpy.load("x.npy"), numpy.load("y.npy")
indices = list(range(len(x)))
random.shuffle(indices)
x, y = x[indices], y[indices]
x, y = numpy.expand_dims(x, 3), numpy.expand_dims(y, 3)
#%%
model = Sequential()
model.add(Conv2D(filters=256, kernel_size=(256, 3), padding="same", activation="relu"))
model.add(MaxPooling2D(pool_size=(1, 2)))
model.add(Conv2D(filters=256, kernel_size=(256, 3), padding="same", activation="relu"))
model.add(MaxPooling2D(pool_size=(1, 2)))
model.compile(optimizer="adam", loss="mae")
History = model.fit(x=x, y=y, batch_size=2, epochs=16, verbose=2, validation_split=0.0625, shuffle=False)