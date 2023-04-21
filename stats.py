from pathlib import Path
import pickle
f = None
def save(data, close=False):
        with open('D:\Python Scripts\CreeperBot\data.pickle', "wb") as f:
            pickle.dump(data, f)
            f.close()
def load():
    f = open('D:\Python Scripts\CreeperBot\data.pickle', "rb")
    d = pickle.load(f)
    f.close()
    return d