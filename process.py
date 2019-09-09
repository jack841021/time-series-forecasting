import json
import arrow

n_days = 30
n_series = 256

with open("saved_charts.json", "r") as saved_charts:
    charts = json.load(saved_charts)
now = arrow.now("Asia/Taipei")
template = { now.shift(days=-i).format("YYYY-MM-DD"): 0 for i in range(n_days, 0, -1) }

series = {}
for chart in charts:
    if "timestamp" in chart["chart"]["result"][0]:
        stamps = chart["chart"]["result"][0]["timestamp"]
        serie = template.copy()
        prices = chart["chart"]["result"][0]["indicators"]["quote"][0]["close"]
        for i in range(len(stamps)):
            date = arrow.Arrow.fromtimestamp(stamps[i]).replace(tzinfo="CST").to("Asia/Taipei").format("YYYY-MM-DD")
            if date in serie:
                serie[date] = prices[i]
        prices = list(serie.values())
        if prices[0] == 0:
            for price in prices[1:]:
                if price != 0:
                    prices[0] = price
        for i in range(len(prices)):
            if prices[i] == 0:
                prices[i] = prices[i - 1]
        series[chart["chart"]["result"][0]["meta"]["symbol"][:4]] = prices

series = sorted(series.items(), key=lambda x: sum(x[1]), reverse=True)[:n_series]
with open("saved_series.json", "w") as saved_series:
    json.dump(series, saved_series)