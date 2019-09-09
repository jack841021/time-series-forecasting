import json
import grequests as g

l_data = "1y" # 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max

base_url = "https://query1.finance.yahoo.com/v8/finance/chart/{}.TW?interval=1d&range={}"

with open("saved_ids.json", "r") as saved_ids:
    ids = json.load(saved_ids)

charts = []
while len(ids):
    batch, ids = ids[:64], ids[64:]
    resps = g.map([g.get(base_url.format(id, l_data)) for id in batch])
    charts += [resp.json() for resp in resps]

with open("saved_charts.json", "w") as saved_charts:
    json.dump(charts, saved_charts)