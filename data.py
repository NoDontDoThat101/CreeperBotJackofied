from pathlib import Path
import os
import json
import discord.ext.tasks as tasks


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
    
