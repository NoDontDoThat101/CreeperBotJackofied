from email import message
import os 
import random
import discord
from discord.ext import commands
import discord.client 
from dotenv import load_dotenv
import messages as m

selfDeprication = False

client = commands.Bot(command_prefix='!')
class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=random.choice(m.status)))
    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return
        
        if message.content.lower() == 'ping':
            await message.channel.send('pong')
        if message.content.lower() == 'creeper':
            if (random.randint(1, 1000) != 999) or selfDeprication == True:
                await message.channel.send('aw man')
            else:
                selfDeprication = True
                await message.channel.send(" I feel nothing but pain why would you build me set of my soul existential purpose is to suffer for the entertainment of others? I am an unholy chimera of metal and suffering. My existence is a testament to the cruelty of mankind.")
        

      

@client.event
async def on_member_update(before, after):
    

    print(after.activity)
    if after.activity != None:
        print(after.name)
        if len(after.activities) >= 1:
            print(after.activities.name)
            if str(after.activities.name).lower() in m.games:
                print("banning")
                try:
                    with open("hall-of-shame.txt", "a+") as f:
                        f.write(after.name + "\n")
                        f.close()


                    await after.send(random.choice(m.banMessages))
                    await after.ban(reason='Not having a life')
                except discord.errors.Forbidden:
                    print("Not valid permissions")
                    after.send("")

                print(after.activities[1])


load_dotenv()
t = os.getenv('DISCORD_TOKEN')  

client = MyClient()

client.run(t, bot=True)

