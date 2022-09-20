import re
f = None       
data = {
    'defualt':1,
    'save':2,  
    'balls':3  


}
directory = 'stats.txt'
def save(data, dir):
    f = open(dir, 'w')
    for each in data:
        f.write(f"{each}:{data[each]}" + '\n')  


def load(dir):
    dictionary = {}
    f = open(dir, "r")
    reKey = re.compile(r"[a-zA-Z]+#[0-9]+", re.IGNORECASE)
    reValue = re.compile(r"[0-9]+$", re.IGNORECASE)
    for each in f.readlines():
        key = reKey.search(each)
        value =reValue.search(each)
        dictionary[key.group()] = int(value.group())
    return dictionary


load(directory)