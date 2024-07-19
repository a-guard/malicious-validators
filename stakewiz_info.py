from requests import get
import orjson


# https://docs.stakewiz.com/reference/api-reference/validators
STAKE_WIZ_API = 'https://api.stakewiz.com/validators?sort=-activated_stake'


with open('data/slot-leader.json', 'r') as f: d = orjson.loads(f.read())
    
identity_l = set()
for (slot, sig) in d.items():
    identity_l.add(sig)

resp = get(STAKE_WIZ_API)
js = orjson.loads(resp.text)

activated_stake = 0
for v in js:
    if v['identity'] in identity_l:
        stake = v['activated_stake']
        print(v['identity'], '%d' % stake, v['name'])
        activated_stake += v['activated_stake']

print('total: %d SOL' % activated_stake)
    