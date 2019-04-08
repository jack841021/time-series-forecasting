import json
import numpy

with open('saved_series.json', 'r') as saved_series:
    series = json.load(saved_series)

series = numpy.array(series)

l_t, l_p = 7 * 8, 7 * 1

xs, ys = [], []
for i in range(len(series[0]) - l_t - l_p + 1):
    xs += [series[:, i : i + l_t]]
    ys += [series[:, i + l_t : i + l_t + l_p]]

xs, ys = numpy.array(xs), numpy.array(ys)

