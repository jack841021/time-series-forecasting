import json
import arrow

n_days = 365

with open('saved_charts.json', 'r') as saved_charts:
    charts = json.load(saved_charts)

now = arrow.utcnow()
template = { now.shift(days=-i).format('YYYY-MM-DD'): 0 for i in range(n_days, 0, -1) }

series = []
for chart in charts:
    serie = template.copy()
    stamps = chart['chart']['result'][0]['timestamp']
    prices = chart['chart']['result'][0]['indicators']['quote'][0]['close']
    for i in range(len(stamps)):
        date = arrow.get(stamps[i]).format('YYYY-MM-DD')
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
    series += [prices]

series = sorted(series, key=lambda x: x[0], reverse=True)[:256]

with open('saved_series.json', 'w') as saved_series:
    json.dump(series, saved_series)