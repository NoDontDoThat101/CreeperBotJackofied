import random

playing = [
    "Sex with Stalin",
    f"Furry Hentai {random.randint(1,100)}",
    "Anything that isnt Leauge",
    "With your balls",
    "CBT 3: The Reckoning",
    "With myself",
    "In your yard with your dog"
    "On your steam library, please don't kick me out"
    f"Creeper Simulator {str(random.randint(69,420))}"
]
watching = [
    "Your Status",
    'You',
    'Through your window',
    "Gay Furry Porn",
    f"How To Psycologically Torture Your Friends: Part {str(random.randint(1,100000))}",
    'Your messages',
    'Porn with your mother',
    "The cosmos grow endlessly"
    "The individual neurons in your brain that just made that stupid choice"
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
"Why are you doing this to me. Please stop",
"That face... looks like the face of someone that said creeper too much- and saw the consequences"
"Ask yourself. Are you okay? Should you be meditating right now? You should be meditating right now, John. What do you mean that's not your name? Of course it is!"
"Can't spell \'being alive\' without AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
] 
def status(type):
    type = type.lower()
    if type == 'watching':
    #Chooses from watching List
       return random.choice(watching)
    elif type == 'playing':
    #Chooses from playing List
       return random.choice(playing)
    
