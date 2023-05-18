import random

games = [
    "leauge of legends",
    "genshin impact",
    "destiny 2",
    "overwatch",
]

playing = [
    "Sex with Stalin",
    f"Furry Hentai {random.randint(1,100)}",
    "Anything that isnt LOL",
    "With your balls",
    "CBT 3: The Reckoning",
    "With myself",
    
]
watching = [
    "Your Status",
    'You',
    "Gay Furry Porn",
    "How To Psycologically Torture Your Friends: Part " + str(random.randint(1,100000)),
    'Your messages' 
]
custom = [
    "I see you",
    "Will you marry me?",
    "Sussy Baka",
    "I Love You ",
    "@whistle, will you marry me?"
]



def status(type):
    type = type.lower()
    if type == 'watching':
    #Chooses from watching List
       return random.choice(watching)
    elif type == 'playing':
    #Chooses from playing List
       return random.choice(playing)
    elif type == 'custom':
        return random.choice(custom)
    