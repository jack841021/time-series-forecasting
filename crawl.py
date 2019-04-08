import json
import requests as r

l = '1mo' # 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max

# http://isin.twse.com.tw/isin/C_public.jsp?strMode=2
with open('saved_ids.json', 'r') as saved_ids:
    ids = json.load(saved_ids)[:10]

charts = []
for id in ids:
    result = r.get('https://query1.finance.yahoo.com/v8/finance/chart/{}.TW?interval=1d&range={}'.format(id, l))
    if result.status_code == 200:
        charts += [result.json()]
    else:
        charts += [None]

with open('saved_charts.json', 'w') as saved_charts:
    json.dump(charts, saved_charts)