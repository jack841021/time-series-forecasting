import json
import numpy

last_min = 20
lx, ly = 7 * 4, 7 * 1

with open("saved_charts.json", "r") as saved_charts:
    charts = json.load(saved_charts)

x, y = [], []
for chart in charts:
    prices = chart["chart"]["result"][0]["indicators"]["quote"][0]["close"]
    if prices[0] == None:
        for price in prices[1:]:
            if price != None:
                prices[0] = price
                break
    for i in range(len(prices)):
        if prices[i] == None:
            prices[i] = prices[i - 1]
    if prices[-1] >= last_min:
        for i in range(len(prices) - lx - ly + 1):
            x += [prices[i: i + lx]]
            y += [prices[i + lx: i + lx + ly]]

x, y = numpy.array(x, dtype="float32"), numpy.array(y, dtype="float32")
maxima = max(numpy.max(x), numpy.max(y))
x, y = x / maxima, y / maxima

numpy.save("x.npy", x)
numpy.save("y.npy", y)