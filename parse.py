import json

# https://isin.twse.com.tw/isin/C_public.jsp?strMode=2
text = ''''''

ids = [line[:4] for line in text.split("\n")]
print(len(ids))

with open("saved_ids.json", "w") as saved_ids:
    json.dump(ids, saved_ids)
