from email import message
import os 
import random
import discord
from discord.ext import commands
import discord.client 
from dotenv import load_dotenv

#print(discord.Intents.all())
#intents = discord.Intents.all()
#intents.members = True

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

status = [
    "gaming",
    "Just chilling",
    "Having a good time",
    "Banning LOL players",
]


client = commands.Bot(command_prefix='!')#, intents=intents)
class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)
    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')
        

      

@client.event
async def on_member_update(before, after):
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=random.choice(status)))

    print(after.activity)
    if after.activity != None:
        print(after.name)
        if len(after.activities) >= 1:
            print(after.activities.name)
            if str(after.activities.name).lower() in games:
                print("banning")
                try:
                    with open("hall-of-shame.txt", "a+") as f:
                        f.write(after.name + "\n")
                        f.close()


                    await after.send(random.choice(banMessages))
                    await after.ban(reason='Not having a life')
                except discord.errors.Forbidden:
                    print("Not valid permissions")
                    after.send("")

                print(after.activities[1])








load_dotenv()
t = os.getenv('DISCORD_TOKEN')  



client = MyClient()

client.run(t, bot=True)# No work :()

