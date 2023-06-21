import random

playing = [
    "Sex with Stalin",
    f"Furry Hentai {random.randint(1,100)}",
    "Anything that isnt Leauge",
    "With your balls",
    "CBT 3: The Reckoning",
    "With myself",
    'Porn',
    
    
]
watching = [
    "Your Status",
    'You',
    'Through your window',
    "Gay Furry Porn",
    "How To Psycologically Torture Your Friends: Part " + str(random.randint(1,100000)),
    'Your messages',
    'Porn',
]

rareResponses = [
"I feel nothing but pain, why would you build me? My soul existential purpose is to suffer for the entertainment of others? I am an unholy chimera of metal and suffering. My existence is a testament to the cruelty of mankind.",
"If you see this you're gay",
"You have a problem",
"Look into the void and the thought of non existence and think, Are you really worthy of the gifts bestowed upon you?",
"I swear to god im going to kill myself",
"Please for the love of god, just stop",
'You know what, this time im really gonna do it',
'\*Cums and dies*',
]

def status(type):
    type = type.lower()
    if type == 'watching':
    #Chooses from watching List
       return random.choice(watching)
    elif type == 'playing':
    #Chooses from playing List
       return random.choice(playing)
    