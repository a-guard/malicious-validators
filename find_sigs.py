from solana.rpc.api import Client
from solders.pubkey import Pubkey
from solders.signature import Signature
import orjson
import json
import os


client = Client(os.getenv('RPC'))


ACCOUNT_PUBKEY = Pubkey.from_string('Ec9xymGeMuURLQfpMsMPkEwy5ktAiQSaFSjF5oJ3kERa')


d = {}
s_l = client.get_signatures_for_address(ACCOUNT_PUBKEY, before=None)
s_l_js = orjson.loads(s_l.to_json())
try:
    while len(s_l_js['result']) > 0:
        for s in s_l_js['result']:
            if s['err'] is not None: continue
                
            sig = s['signature']
            slot = s['slot']
            d[sig] = slot
            
        print('lsig:', sig, 'slot:', slot, 'len:', len(d))
        s_l = client.get_signatures_for_address(ACCOUNT_PUBKEY, before=Signature.from_string(sig))
        s_l_js = orjson.loads(s_l.to_json())
except: pass

with open('data/signature-slot.json', 'w') as f:
    f.writelines(json.dumps(d, indent=4))
