from requests import get
import orjson


STAKE_WIZ_API = 'https://api.stakewiz.com/validators'


with open('data/slot-leader.json', 'r') as f:
    d = orjson.loads(f.read())
    
identity_l = set()
for (slot, sig) in d.items():
    identity_l.add(sig)

resp = get(STAKE_WIZ_API)
js = orjson.loads(resp.text)

activated_stake = 0
for v in js:
    if v['identity'] in identity_l:
        print(v['identity'], v['activated_stake'])
        activated_stake += v['activated_stake']

print(activated_stake)
    