import orjson


with open('data/slot-leader.json', 'r') as f: d = orjson.loads(f.read())
    
unique_indetity_l = set()
for (slot, sig) in d.items(): unique_indetity_l.add(sig)

with open('data/unique_identity_list.txt', 'w') as f: f.writelines('\n'.join(list(unique_indetity_l)))
