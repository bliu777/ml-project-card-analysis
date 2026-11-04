import numpy as np
import requests
import json
import os

def import_set_card_data(setcode: str):
    setcode = setcode.upper()
    s = requests.Session()
    url = "https://api.scryfall.com/cards/search?q=s:" + setcode.lower()
    payload = {'include_extras': 'false', 'unique': 'cards'}
    req = requests.Request('GET', url, params=payload)
    r = req.prepare()
    #print(r.headers)

    r.headers = {'User-Agent': 'ml-card-eval/1.0', 'Accept-Encoding': 'gzip, deflate, br, zstd', 'Accept': '*/*', 'Connection': 'keep-alive'}
    
    resp = s.send(r)
    #print(resp.url)

    #print(r.headers)

    if resp.status_code == 204:
        raise Exception("Invalid set code!")

    (base_path, _) = os.path.split(os.getcwd())
    set_data_path = os.path.join(base_path, 'data', setcode)
    if not os.path.exists(set_data_path):
        os.mkdir(set_data_path)

    with open(os.path.join(set_data_path, setcode.lower() + '_cards'), 'w') as f:
        f.write(json.dumps(resp.json(), indent=4))

    return