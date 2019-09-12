import json
import arrow
import traceback

n_days = 365
n_series = 256

with open("saved_charts.json", "r") as saved_charts:
    charts = json.load(saved_charts)

then = arrow.now("+08:00").shift(days=-n_days)
template = {then.shift(days=i).format("YYYY-MM-DD"): 0 for i in range(n_days)}

series = {}
for chart in charts:
    if chart["chart"]["result"][0]["meta"]["firstTradeDate"] < then.timestamp:
        stamps = chart["chart"]["result"][0]["timestamp"]
        serie = template.copy()
        prices = chart["chart"]["result"][0]["indicators"]["quote"][0]["close"]
        for i in range(len(stamps)):
            date = arrow.Arrow.fromtimestamp(stamps[i]).replace(tzinfo="-08:00").to("+08:00").format("YYYY-MM-DD")
            if date in serie and isinstance(prices[i], float):
                serie[date] = prices[i]
        prices = list(serie.values())
        if prices[0] == 0:
            for price in prices[1:]:
                if price != 0:
                    prices[0] = price
                    break
        for i in range(len(prices)):
            if prices[i] == 0:
                prices[i] = prices[i - 1]
        series[chart["chart"]["result"][0]["meta"]["symbol"][:4]] = prices

series = sorted(series.items(), key=lambda x: sum(x[1]), reverse=True)[:n_series]
print(series[-1])

with open("saved_series.json", "w") as saved_series:
    json.dump(series, saved_series)