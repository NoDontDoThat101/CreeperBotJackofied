from pathlib import Path
from os import path
import json

def updateStat(guild,uid, value=1):
    json_data = load(guild)
    print(json_data)
    json_data[guild][uid] += value
    save(json_data)
    return json_data[guild][uid]
    
        
def load(guild):
    try:
        with open(path.join(Path(__file__).parent.absolute(),"stats.json"),'r+') as f:
            data = json.load(f)
            if guild in data:
                print(data)
                return data
            else:
                data[guild] = {}
                print(data)
                return data
    except FileNotFoundError:
        with open(path.join(Path(__file__).parent.absolute(),"stats.json"),'x') as f:
            data = {}
            data[guild] = {}
            print(data)
            return data
    
def save(json_data):
    with open(path.join(Path(__file__).parent.absolute(),"stats.json"), "w") as f:
        f.write(json.dumps(json_data,f, indent=4))

