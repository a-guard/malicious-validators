from requests import Session
from concurrent.futures import ThreadPoolExecutor
import orjson
import json
import os


RPC_URL: str = os.getenv('RPC')


s = Session()
s.headers.update({ 'Accept': 'application/json', 'Content-Type': 'application/json' })


slot_and_leaders = dict()


def get_slot_leader(slot):
    payload = {'jsonrpc': '2.0', 'id': 1, 'method': 'getBlock', 'params': [
        int(slot), {'encoding': 'json', 'maxSupportedTransactionVersion': 0, 'transactionDetails': 'none', 'rewards': True}
    ]}
    resp = s.post(url=RPC_URL, data=orjson.dumps(payload))
    js = orjson.loads(resp.text)
    pubkey: str = js['result']['rewards'][0]['pubkey']
    slot_and_leaders[slot] = pubkey


with open('data/filtered_sandwitches.json', 'r') as f:
    d = orjson.loads(f.read())

with ThreadPoolExecutor(max_workers=600) as pool:
    for _ in pool.map(
        get_slot_leader, list(d)
    ): pass

with open('data/slot-leader.json', 'w') as f:
    f.writelines(json.dumps(slot_and_leaders, indent=4))
