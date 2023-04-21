from pathlib import Path
import pickle
f = None       
data = {
    'defualt':1,
    'save':2,  
    'balls':3  
}

def save(data, close=False):
        path = Path(__file__).parent
        with path.open("data.pickle", "wb") as f:
            pickle.dump(data, f)
            f.close()

def load():
    path = Path(__file__).parent
    with path.open("data.pickle", "rb") as f:
        d = pickle.load(f)
        f.close()
        return d

save(data)