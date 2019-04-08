import json
import grequests as g

n_ids = 1000
l_data = '1mo' # 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max

with open('saved_ids.json', 'r') as saved_ids:
    ids = json.load(saved_ids)[:n_ids]
base_url = 'https://query1.finance.yahoo.com/v8/finance/chart/{}.TW?interval=1d&range={}'

charts = []
while len(ids):
    batch, ids = ids[:64], ids[64:]
    results = g.map([g.get(base_url.format(id, l_data)) for id in batch])
    charts += [result.json() for result in results]

with open('saved_charts.json', 'w') as saved_charts:
    json.dump(charts, saved_charts)