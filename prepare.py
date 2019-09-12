import json
import numpy

l_x, l_y = 7 * 4, 7 * 1

with open("saved_series.json", "r") as saved_series:
    series = json.load(saved_series)

series = numpy.array([serie[1] for serie in series], dtype="float32")
maxima = numpy.max(series)
series = series / maxima
print(maxima)

x, y = [], []
for i in range(series.shape[1] - l_x - l_y + 1):
    x += [series[:, i: i + l_x]]
    y += [series[:, i + l_x: i + l_x + l_y]]

numpy.save("x.npy", x)
numpy.save("y.npy", y)