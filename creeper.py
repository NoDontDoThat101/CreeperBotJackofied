import os 
import random
from typing import Any
import discord
from discord.enums import Status
from discord.ext import commands, tasks
from discord.utils import get
import discord.client
from discord.flags import Intents 
from dotenv import load_dotenv
import messages as lM
import stats
import logging
import pprint
import asyncio
import os
from os import path
from pathlib import Path
load_dotenv()




#Get All Sus Variable From enviroment 

jackieID = int(os.getenv('JACKIE_ID'))
voidID = int(os.getenv('VOID_ID'))
testid = int(os.getenv('TEST_ID'))

#Misc Variables
testing = False
intents = discord.Intents.all()
keywords = ['Suzuka', f'<@{voidID}>']
client = commands.Bot(command_prefix='!',intents=intents)
value = 1
stat = 0

if os.path.isfile(r'CreeperBot\testing.txt'):
    token = os.getenv('TEST_TOKEN')
    testing = True
else:
    token = os.getenv('TOKEN')
    testing = False
class MyClient(discord.Client):

    @tasks.loop(seconds=10)
    async def status_change(self):
        await client.wait_until_ready()
        r = random.randint(0,1)
        if random.randint(0,1) == 0:
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=lM.status('playing')))
        elif r == 1:    
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=lM.status('watching')))
#        else: 
#            await client.change_presence(activity=discord.Activity(type= discord.ActivityType.custom,name=m.status('custom')))
        
        
    
    @client.event
    async def on_ready(self):
        print('Logged on as', self.user, 'on discord version', discord.__version__)
        await self.status_change.start()
                
        
    @client.event
    async def on_message(self, message):
        dm = discord.channel.DMChannel
        m = message.content.lower()
        M = message.content
        channel = message.channel
        authID = message.author.id
        guild = str(message.guild.id)
        
        if message.author.id == (self.user.id or testid):   #Bot will not reply to itself, on top so nothing will mess with it
            return
        if 'vent' in channel.name.lower(): #Will not reply to any message if the channel has vent in it
            return
        if testing:
            if m == 'ping':                    #Test message to ensure its reciving
                await message.reply('pong')
                
        if '!stats' in m:                   #Statistics
            if not bool(message.mentions):
                v = stats.getStat(guild, str(message.author.id))
                if (v <= 500):
                    await message.reply( f'You have said creeper {v} times')

                if v == (None or 0):
                    await message.reply(f"<@{uid}> hasn't said creeper yet")
            else:
                for uids in message.mentions:
                    v = stats.getStat(guild, str(uids.id))
                    await message.reply(f'<@{uids.id}> has said creeper {v} times')
                    
        #Whole premise of the bot
        if 'creeper' in m:
            guild = str(message.guild.id)
            uid = str(authID)
            creepers = m.count('creeper')
            if (random.randint(1, 1000) != 999):
               #Random chance creeper
                await message.reply(f'aw man\n'*int(creepers))
                stat = stats.updateStat(guild, uid, creepers)
                print("Replied to", message.author.name, f"They've done this {stat} times")
            else:
                rareMessage = random.choice(lM.rareMessages)
                await channel.send(rareMessage)
                stats.updateStat(guild, uid, int(creepers)*3)
            role = discord.utils.get(message.guild.roles, name='CreeperNotifs')
            try:
                if role not in message.author.roles:
                    await message.author.add_roles(role)
                    print(f'Gave role to {message.author}')
            except Exception as e:
                print(e, 'Line 117')

#Start Logging
handler = logging.FileHandler(filename=path.join(Path(__file__).parent.absolute(), 'discord.log'), encoding='utf-8', mode='w')


#Start Bot
client = MyClient(intents=intents)
client.run(token, log_handler=handler, log_level=logging.INFO)