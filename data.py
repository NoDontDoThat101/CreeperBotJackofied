from pathlib import Path
import os
import json
import discord
import discord.ext.tasks as tasks

def checkConfig(value):
    if value == 'False':
        return False
    elif value == 'True':
        return True

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

def sync(verbose, dir):
    try:
        with open(dir,'r') as f:
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
    
@tasks.loop(hours=24)
async def backup(client, channelID):
    if os.path.isfile(os.path.join(Path(__file__).parent.absolute(), 'stats.json')):
        try:
            channel = client.get_channel(channelID)
            await channel.send(file=discord.File(os.path.join(Path(__file__).parent.absolute(), 'stats.json')))
        except Exception as e:
            print('Backup Failed\n', e)
            backup.cancel()

        
def extractID(string):
    #String = 'num, num, num'
    integers = []
    split_string = string.split(',')
    #Split_string = ['num', 'num', 'num']
    for num in split_string:
        num = num.strip()
        if num.isdigit():
            integers.append(int(num))
    return integers


                
