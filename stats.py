from pathlib import Path
from os import path
import pickle
import pdb

f = None
def updateStat(uid, value=1):
    if type(uid) != str:
        try:
            uid = str(uid)
        except Exception as e:
            print(e)
    if type(value) != int:
        try:
            value = int(value)
        except Exception as e:
            print(e)
    d = load()
    if d == {}:
        d = {uid: value}
        save(d)
        return d[uid]
    d[uid] = d[uid] + value
    save(d)
    return d[uid]

def save(data, close=False):
    with open('D:\Python Scripts\CreeperBot\data.pickle', "wb") as f:
        pickle.dump(data, f)
        f.close()

        
def load():
    if not path.exists('D:\Python Scripts\CreeperBot\data.pickle'):
        f = open('D:\Python Scripts\CreeperBot\data.pickle', "x")
        f.close()
        return {}
    f = open('D:\Python Scripts\CreeperBot\data.pickle', "rb")
    try:
        d = pickle.load(f)  
    except EOFError:
        f.close()
        print ("No data found, returning empty dict")
        return {}
    f.close()

    return d
