import orjson


with open('data/slot-leader.json', 'r') as f:
    d = orjson.loads(f.read())
    
schindler_list = set()
for (slot, sig) in d.items():
    schindler_list.add(sig)

with open('data/schindler_list.txt', 'w') as f:
    f.writelines('\n'.join(list(schindler_list)))
