from concurrent.futures import ThreadPoolExecutor
from requests import Session
from traceback import format_exc
import orjson
import json
import time
import os


RPC_URL: str = os.getenv('RPC')
s = Session()
s.headers.update({ 'Accept': 'application/json', 'Content-Type': 'application/json' })

jito_tip_accs = ['Cw8CFyM9FkoMi7K7Crf6HNQqf4uEMzpKw6QNghXLvLkY', 'ADaUMid9yfUytqMBgopwjb2DTLSokTSzL1zt6iGPaS49', '3AVi9Tg9Uo68tJfuvoKvqKNWKkC5wPdSSdeBnizKZ6jT', 'HFqU5x63VTqvQss8hp11i4wVV8bD44PvwucfZ2bU7gRe', 'DfXygSm4jCyNCybVYYK6DwvWqjKee8pbDmJGcLWNDXjh', 'ADuUkR4vqLUMWXxW9gh6D6L8pMSawimctcNZ5pGwDcEt', '96gYZGLnJYVFmbjzopPSU6QiEV5fGqZNyN9nmNhvrZU5', 'DttWaMuVvTiduZRnguLF7jNxTgiMBZ1hyAumKUiL2KRL']
    
RAYDIUM_ACC = '675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8'
RAYDIUM_AUTH = '5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1'
WSOL_MINT = 'So11111111111111111111111111111111111111112'


balance_flow = {}


def filter_tx(sig, trys: int = 0):
    if trys > 10: return
    try:
        # This lib have big number of bugs and very bad perf
        # resp = client.get_transaction(Signature.from_string(sig), max_supported_transaction_version=0)
        payload = {'jsonrpc': '2.0', 'id': 1, 'method': 'getTransaction', 'params': [
            sig, {'maxSupportedTransactionVersion': 0, 'encoding': 'json'},
        ]}
        resp = s.post(url=RPC_URL, data=orjson.dumps(payload))
        if resp.status_code != 200: print(resp)
        js = orjson.loads(resp.text)['result']
        # print(js)
    except KeyboardInterrupt: return
    except:
        print(resp.text)
        print(format_exc())
        time.sleep(1)
        return filter_tx(sig, trys=trys+1)
    
    slot = int(js['slot'])
    
    has_ray = False
    has_jito = False
    for acc in js['transaction']['message']['accountKeys']:
        if acc == RAYDIUM_ACC: has_ray = True
        if acc in jito_tip_accs: has_jito = True
        if has_ray and has_jito: break
    if not has_ray or has_jito: return
    
    for pre_balance in js['meta']['preTokenBalances']:
        if pre_balance['mint'] == WSOL_MINT: continue
        if pre_balance['owner'] == RAYDIUM_AUTH: break
    for post_balance in js['meta']['postTokenBalances']:
        if post_balance['mint'] == WSOL_MINT: continue
        if post_balance['owner'] == RAYDIUM_AUTH: break
    try:
        if pre_balance['mint'] != post_balance['mint'] or pre_balance['owner'] != post_balance['owner']: return
    except UnboundLocalError: return
    
    tx_mint = pre_balance['mint']
    tx_coin_flow = abs(int(pre_balance['uiTokenAmount']['amount']) - int(post_balance['uiTokenAmount']['amount']))
    if tx_coin_flow == 0: return
    
    if slot not in balance_flow:                        balance_flow[slot] = {}
    if tx_mint not in balance_flow[slot]:               balance_flow[slot][tx_mint] = {}
    if tx_coin_flow not in balance_flow[slot][tx_mint]: balance_flow[slot][tx_mint][tx_coin_flow] = []
    balance_flow[slot][tx_mint][tx_coin_flow].append(sig)

t = time.time()

with open('data/signature-slot.json', 'r') as f: d = orjson.loads(f.read())
    
sigs = []
for (sign, slot) in d.items(): sigs.append(sign)

try:
    with ThreadPoolExecutor(max_workers=1500) as pool:
        for _ in pool.map(
            # filter_tx, ['3YE8zQs1NFmUxhbFvEfPu6ZH1YXEFSRvDrjA4aZuFA2c1suSBr8gK1XBwwkJUT1A8MyFoDGBRTF6kFz1gN1JvWyo', '2FwnMsaaXkT7kG2JmSGLyEvYzTpMhJqknWe8kx7EK5jnf4obScbaZuk5c3f6inBQndjic1jwsWDCfup9DqWSRTXV']
            filter_tx, sigs
        ): pass
except: print(format_exc())

# print(balance_flow)
d = {}
for slot in balance_flow:
    for tx_mint in balance_flow[slot]:
        for tx_coin_flow in balance_flow[slot][tx_mint]:
            if len(balance_flow[slot][tx_mint][tx_coin_flow]) != 2: continue
            if slot not in d: d[slot] = []
            d[slot].append((balance_flow[slot][tx_mint][tx_coin_flow]))

with open('data/filtered_sandwitches.json', 'w') as f: f.writelines(json.dumps(d, indent=4))

print('done in %d mins' % ((time.time() - t) // 60))
