import random

    

banMessages = [
    "Stop playing league of legends",
    "Take a shower",
    "Among us??? Sussy??? Imposter?????"
]


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
]

custom = [
    "I see you",
    "Will you marry me?",
    "Sussy Baka",
    "I Love You ",
    "@whistle, will you marry me?"
]

watching = [
    "Your Status",
    'You',
    "Gay Furry Porn",
    "How To Psycologically Torture Your Friends: Part " + str(random.randint(1,100000)), 
]

def status():
    presence = random.randint(1,2)
    if presence == 1:
    #Chooses from watching List
       return random.choice(watching)
    if presence == 2:
    #Chooses from playing List
       return random.choice(playing)
    