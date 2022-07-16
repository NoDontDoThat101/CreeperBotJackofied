from email import message
import os 
import random
import discord
from discord.ext import commands
import discord.client 
from dotenv import load_dotenv
import messages as m



client = commands.Bot(command_prefix='!')
class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)
    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content.lower() == 'ping':
            await message.channel.send('pong')
        if message.content.lower() == 'creeper':
            await message.channel.send('aw man')
        

      

@client.event
async def on_member_update(before, after):
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=random.choice(m.status)))

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

client.run(t, bot=True)# No work :()

