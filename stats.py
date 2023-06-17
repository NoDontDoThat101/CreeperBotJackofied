from data import load, save

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