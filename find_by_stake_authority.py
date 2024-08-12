from requests import get
import orjson
import time


# https://docs.stakewiz.com/reference/api-reference/validators
STAKE_WIZ_API: str = 'https://api.stakewiz.com/'
SFDP_STAKE_AUTH: str = 'mpa4abUkjQoAvPzREkh5Mo75hZhPFQ2FSH6w7dWKuQ5'


def check_stake_by_vote(vote_acc: str, stake_auth: str) -> float:
    r = get(STAKE_WIZ_API + 'validator_stakes/' + vote_acc)
    if r.status_code != 200: 
        print(r)
        return
    js = orjson.loads(r.text)
    
    stake = 0
    for i in js:
        if i['stake_authority'] != stake_auth: continue
        stake += i['active_stake']
    return stake/10**9


def count_sandwitches(identity_acc: str):
    n: int = 0
    for block in filtered_sandwitches:
        if d[block] != identity_acc: continue
        n += len(filtered_sandwitches[block])
        # print(block, len(filtered_sandwitches[block]))
    return n


with open('data/slot-leader.json', 'r') as f: d = orjson.loads(f.read())

with open('data/filtered_sandwitches.json', 'r') as f: filtered_sandwitches = orjson.loads(f.read())
    
identity_l = set()
for (slot, sig) in d.items():
    identity_l.add(sig)

resp = get(STAKE_WIZ_API + 'validators?sort=-activated_stake')
js = orjson.loads(resp.text)

activated_stake = 0
delegated_by_stake = 0
sandwitches_total = 0
for v in js:
    if v['identity'] in identity_l:
        stake = v['activated_stake']
        delegated = check_stake_by_vote(v['vote_identity'], SFDP_STAKE_AUTH)
        time.sleep(0.1) # to prevent rate limiting
        if delegated == 0: continue
        sandwitches_n = count_sandwitches(v['identity'])
        sandwitches_total += sandwitches_n
        activated_stake += v['activated_stake']
        delegated_by_stake += delegated
        print(v['identity'], v['vote_identity'], '{:_}'.format(int(delegated)), sandwitches_n)

print('total sandwitches:', sandwitches_total)
print('total: {:_} SOL'.format(int(activated_stake)))
print('delegated by SFDP: {:_} SOL'.format(int(delegated_by_stake)))
