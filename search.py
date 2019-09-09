#%%
import numpy
import random
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense
from hyperopt import hp, fmin, tpe, space_eval
#%%
def loss(ps):
    model = Sequential()
    model.add(Conv1D(filters=ps["depth"], kernel_size=ps["ksize"], padding="same", data_format="channels_first", activation=ps["activ"]))
    model.add(MaxPooling1D(data_format="channels_first"))
    model.add(Conv1D(filters=ps["depth"], kernel_size=ps["ksize"], padding="same", data_format="channels_first", activation=ps["activ"]))
    model.add(MaxPooling1D(data_format="channels_first"))
    model.add(Flatten(data_format="channels_first"))
    model.add(Dense(units=y.shape[1]))
    model.compile(optimizer="nadam", loss="mae")
    History = model.fit(x=x, y=y, batch_size=2, epochs=16, verbose=2, validation_split=0.0625, shuffle=False)
    return numpy.mean(sorted(History.history["val_loss"])[:2])
# n_layers, optimizer, batch_size, epochs
#%%
x, y = numpy.load("x.npy"), numpy.load("y.npy")
shape = y.shape
y = numpy.reshape(y, (shape[0], shape[1] * shape[2]))
indices = [i for i in range(len(x))]
random.shuffle(indices)
x, y = x[indices], y[indices]
#%%
ps = {
    "depth": hp.choice("depth", [64, 128, 256]),
    "ksize": hp.choice("ksize", [3, 5, 7]),
    "activ": hp.choice("activ", ["softsign", "relu", "tanh", "sigmoid", "exponential", "linear"]),
}
#%%
best = fmin(fn=loss, space=ps, algo=tpe.suggest, max_evals=27)
print(space_eval(ps, best))
