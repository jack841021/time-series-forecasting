import json
import matplotlib.pyplot as plt

lower, upper = 0, 100

with open("saved_charts.json", "r") as saved_charts:
    charts = json.load(saved_charts)

hist = {str(i): 0 for i in range(lower, upper, 10)}
for chart in charts:
    price = chart["chart"]["result"][0]["indicators"]["quote"][0]["close"][-1]
    key = str(int(price / 10) * 10)
    if key in hist:
        hist[key] += 1

plt.plot(list(range(lower, upper, 10)), list(hist.values()))
plt.show()