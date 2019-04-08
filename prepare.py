import json
import numpy

l_t, l_p = 7 * 2, 7 * 1

with open('saved_series.json', 'r') as saved_series:
    series = json.load(saved_series)
series = numpy.array([serie[1] for serie in series])

xs, ys = [], []
for i in range(len(series[0]) - l_t - l_p + 1):
    xs += [series[:, i : i + l_t]]
    ys += [series[:, i + l_t : i + l_t + l_p]]

numpy.save('xs', xs)
numpy.save('ys', ys)
