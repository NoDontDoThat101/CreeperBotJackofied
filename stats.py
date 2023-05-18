from pathlib import Path
from os import path
import json

def updateStat(guild,uid, value=1):
    guild = str(guild)
    uid = str(uid)
    json_data = load(guild)
    if uid not in json_data[guild]:
        json_data[guild][uid] = 1
        save(json_data)
        print(json_data)
        print(json_data[guild][uid])
        return json_data[guild][uid]
    else:
        json_data[guild][uid] += value
        save(json_data)
        print(json_data)
        print(json_data[guild][uid])
        return json_data[guild][uid]

def getStat(guild,uid):
    guild = str(guild)
    uid = str(uid)
    json_data = load(guild)
    if uid in json_data[guild]:
        return json_data[guild][uid]
    else:
        return 0
        
def load(guild):
    try:
        with open(path.join(Path(__file__).parent.absolute(),"stats.json"),'r+') as f:
            data = json.load(f)
            if guild in data:
                return data
            else:
                data[guild] = {}
                return data
    except FileNotFoundError:
        with open(path.join(Path(__file__).parent.absolute(),"stats.json"),'x') as f:
            data = {}
            data[guild] = {}
            return data
    
def save(json_data):
    with open(path.join(Path(__file__).parent.absolute(),"stats.json"), "w") as f:
        f.write(json.dumps(json_data, indent=4))

