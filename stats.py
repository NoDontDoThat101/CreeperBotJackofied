from pathlib import Path
import os
import json

def getAllStats(guild):
    guild = str(guild)
    json_data = load(guild)
    return json_data[guild]

def updateStat(guild,uid, value=1):
    guild = str(guild)
    uid = str(uid)
    json_data = load(guild)
    if uid not in json_data[guild]:
        json_data[guild][uid] = 1
        save(json_data)
        return json_data[guild][uid]
    else:
        json_data[guild][uid] += value
        save(json_data)
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
    data = {}
    try:
        with open(os.path.join(Path(__file__).parent.absolute(),"stats.json"),'r+') as f:
            data = json.load(f)
            if guild in data:
                return data
            else:
                data[guild] = {}
                return data
    except FileNotFoundError:
        with open(os.path.join(Path(__file__).parent.absolute(),"stats.json"),'x') as f:
            data = {}
            data[guild] = {}
            return data
    
def save(json_data):
    with open(os.path.join(Path(__file__).parent.absolute(),"stats.json"), "w") as f:
        f.write(json.dumps(json_data, indent=4))

def sync(verbose):
    if os.path.isfile(os.path.join(Path(__file__).parent.absolute(), 'sync.txt')):
        try: 
            with open(os.path.join(Path(__file__).parent.absolute(),'sync.txt'),'r') as f:
                networkStat = f.readline()
        except Exception as e:
            print(e)
        try:
            with open(networkStat,'r') as f:
                json_data = json.load(f)
                save(json_data)
                if verbose:
                    print("Synced")
        except OSError as e:
            if verbose:
                print("Sync Failed, destination unreachable")
                return
        except Exception as e:
            if verbose:
                print("Sync Failed")
                print(e)
            return
    else:
        if verbose:
            print("Sync Failed:", end=' ')
            print("No sync file")
        return
                
def resetStat(guild, uid):
    guild = str(guild)
    uid = str(uid)
    json_data = load(guild)
    json_data[guild][uid] = 0
    save(json_data)
    return json_data[guild][uid]


def resetAll(guild):
    if input("Are you sure you want to reset all stats? (y/n)") == "y":
        guild = str(guild)
        try:
            json_data = load(guild)
        except Exception as e:
            print(e)
            return False
        for uid in json_data[guild]:
            json_data[guild][uid] = 0
        try:
            save(json_data)
        except Exception as e:
            print(e)
            return False
        return True
    else: 
        return False