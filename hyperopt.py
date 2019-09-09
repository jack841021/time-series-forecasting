#%%
import numpy
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense
from hyperopt import hp, fmin, tpe, space_eval
from actitools import reduce
#%%
ps = {
    "depth": hp.choice("depth", [16, 32, 64]),
    "ksize": hp.choice("ksize", [3, 5, 7]),
    "activ": hp.choice("activ", ["elu", "selu", "relu"]),
    "optim": hp.choice("optim", ["Adam", "Adamax", "Nadam"]),
}
#%%
x, y = numpy.load("x.npy"), numpy.load("y.npy")
max_x, max_y = max(x), max(y)
x, y = x / max_x, y / max_y
max_x, max_y
#%% 
def loss(ps):
    model = Sequential([
        Conv1D(filters=ps["depth"], kernal_size=ps["ksize"], activation=ps["activ"]),
        MaxPooling1D(),
        Flatten(),
        Dense(units=len(ys[0]))
    ])
    model.compile(optimizer=ps["optim"], loss="mae")
    History = model.fit(x=x, y=y, batch_size=2, epochs=64, validation_split=0.0625, shuffle=True)
    return numpy.mean(sorted(History.history["val_loss"])[:4])
# DOTO: dropout, n_layers, 
#%%
best = fmin(fn=loss, space=ps, algo=tpe.suggest, max_evals=int(reduce(lambda x, y: x * y, [len(v) for v in ps.values()]) / 2))
space_eval(ps, best)