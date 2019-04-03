import json

with open('history.json','r') as f:
    print(json.load(f))