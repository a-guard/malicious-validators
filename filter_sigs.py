from concurrent.futures import ThreadPoolExecutor
from solana.rpc.api import Client
from solders.signature import Signature
from solders.pubkey import Pubkey
from traceback import format_exc
import orjson
import json
import time
import os


client = Client(os.getenv('RPC'))

jito_tip_accs = ['Cw8CFyM9FkoMi7K7Crf6HNQqf4uEMzpKw6QNghXLvLkY', 'ADaUMid9yfUytqMBgopwjb2DTLSokTSzL1zt6iGPaS49', '3AVi9Tg9Uo68tJfuvoKvqKNWKkC5wPdSSdeBnizKZ6jT', 'HFqU5x63VTqvQss8hp11i4wVV8bD44PvwucfZ2bU7gRe', 'DfXygSm4jCyNCybVYYK6DwvWqjKee8pbDmJGcLWNDXjh', 'ADuUkR4vqLUMWXxW9gh6D6L8pMSawimctcNZ5pGwDcEt', '96gYZGLnJYVFmbjzopPSU6QiEV5fGqZNyN9nmNhvrZU5', 'DttWaMuVvTiduZRnguLF7jNxTgiMBZ1hyAumKUiL2KRL']
jito_tip_accs = [Pubkey.from_string(i) for i in jito_tip_accs]
    
RAYDIUM_ACC = Pubkey.from_string('675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8')
RAYDIUM_AUTH = Pubkey.from_string('5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1')
WSOL_MINT = Pubkey.from_string('So11111111111111111111111111111111111111112')


balance_flow = {}


def filter_tx(sig, trys: int = 0):
    if trys > 30: return
    try:
        resp = client.get_transaction(Signature.from_string(sig), max_supported_transaction_version=0)
    except KeyboardInterrupt: return
    except:
        print(format_exc())
        time.sleep(5)
        return filter_tx(sig, trys=trys+1)
    
    slot = resp.value.slot
    
    has_ray = False
    has_jito = False
    for acc in resp.value.transaction.transaction.message.account_keys:
        if acc == RAYDIUM_ACC: has_ray = True
        if acc in jito_tip_accs: has_jito = True
        if has_ray and has_jito: break
    if not has_ray or has_jito: return
    
    for pre_balance in resp.value.transaction.meta.pre_token_balances:
        if pre_balance.mint == WSOL_MINT: continue
        if pre_balance.owner == RAYDIUM_AUTH: break
    for post_balance in resp.value.transaction.meta.post_token_balances:
        if post_balance.mint == WSOL_MINT: continue
        if post_balance.owner == RAYDIUM_AUTH: break
    try:
        if pre_balance.mint != post_balance.mint or pre_balance.owner != post_balance.owner: return
    except UnboundLocalError: return
    
    tx_mint = str(pre_balance.mint)
    tx_coin_flow = abs(int(pre_balance.ui_token_amount.amount) - int(post_balance.ui_token_amount.amount))
    
    if slot not in balance_flow:                        balance_flow[slot] = {}
    if tx_mint not in balance_flow[slot]:               balance_flow[slot][tx_mint] = {}
    if tx_coin_flow not in balance_flow[slot][tx_mint]: balance_flow[slot][tx_mint][tx_coin_flow] = []
    balance_flow[slot][tx_mint][tx_coin_flow].append(sig)
    

with open('data/signature-slot.json', 'r') as f:
    d = orjson.loads(f.read())
    
sigs = []
for (sign, slot) in d.items():
    sigs.append(sign)

try:
    with ThreadPoolExecutor(max_workers=200) as pool:
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

with open('data/filtered_sandwitches.json', 'w') as f:
    f.writelines(json.dumps(d, indent=4))

print('done')