import json

with open("sjj_mg.json", 'r') as f:
    data = json.load(f)

print(len(data))

for i in range(len(data)):
    data[i]['id'] = i + 1

with open("sjj_mg.json", 'w') as f:
    json.dump(data, f, indent=4)  


