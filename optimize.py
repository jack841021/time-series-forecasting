#%%
import numpy
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense
from hyperopt import hp, fmin, tpe, space_eval
#%%
ps = {
    "depth": hp.choice("depth", [16, 32, 64]),
    "ksize": hp.choice("ksize", [3, 5, 7]),
    "activ": hp.choice("activ", ["elu", "selu", "relu"]),
    "optim": hp.choice("optim", ["Adam", "Adamax", "Nadam"]),
}
#%% 
def loss(ps):
    model = Sequential()
    model.add(Conv1D(filters=ps["depth"], kernel_size=ps["ksize"], data_format="channels_first", activation=ps["activ"]))
    model.add(MaxPooling1D(data_format="channels_first"))
    model.add(Conv1D(filters=ps["depth"], kernel_size=ps["ksize"], data_format="channels_first", activation=ps["activ"]))
    model.add(MaxPooling1D(data_format="channels_first"))
    model.add(Flatten())
    model.add(Dense(units=y.shape[1]))
    model.compile(optimizer=ps["optim"], loss="mae")
    History = model.fit(x=x, y=y, batch_size=2, epochs=64, validation_split=0.0625, shuffle=True, verbose=2)
    return numpy.mean(sorted(History.history["val_loss"])[:4])
#%%
x, y = numpy.load("x.npy"), numpy.load("y.npy")
best = fmin(fn=loss, space=ps, algo=tpe.suggest, max_evals=41)
space_eval(ps, best)