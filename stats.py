from pathlib import Path
import pickle
import pdb
f = None
data = {'341767947309678603':214}
def updateStat(uid, value=1):
    if type(uid) is not str:
        try:
            uid = str(uid)
        except: TypeError("uid must be a string")
        
    if type(value) is not int:
        raise TypeError("value must be an integer")
    f = open('D:\Python Scripts\CreeperBot\data.pickle', "rwb")
    d  = pickle.load(f)
    d[uid] = d[uid]+value
    pickle.dump(d, f)
    f.close()
    return d[uid]

def save(data, close=False):
    with open('D:\Python Scripts\CreeperBot\data.pickle', "wb") as f:
        pickle.dump(data, f)
        f.close()
def load():
    f = open('D:\Python Scripts\CreeperBot\data.pickle', "rb")
    try:
        d = pickle.load(f)  
    except EOFError:
        f.close()
        print ("No data found, returning empty dict")
        return {}
    f.close()
    return d
