import json
import re

with open('hotels.json', encoding="utf-8") as f:
    data = json.load(f)

for h in data:
    h['__k'] = re.sub(r'^(the|a|an)\s+', '', h['Name'].strip(), flags=re.I).lower()

data.sort(key=lambda h: h['__k'])

for h in data:
    del h['__k']

with open('hotels.json', 'w', encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write('\n')

print('Sorted', len(data), 'hotels')
