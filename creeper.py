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
import unicodedata
load_dotenv()
sync = path.isfile(path.join(Path(__file__).parent.absolute(), 'sync.txt'))

#Misc Variables
testing = None
testid = int(os.getenv('TEST_ID'))
intents = discord.Intents.all()
client = commands.Bot(command_prefix='!',intents=intents)
value = 1
stat = 0

if path.isfile(path.join(Path(__file__).parent.absolute(), 'testing.txt')):
    token = os.getenv('TEST_TOKEN')
    testing = True
    if sync:
        stats.sync(True)
else:
    token = os.getenv('TOKEN')
    testing = False
    if sync:
        stats.sync(False)

class MyClient(discord.Client):
    

    @tasks.loop(seconds=60)
    async def status_change(self):
        await client.wait_until_ready()
        r = random.randint(0,1)
        if random.randint(0,1) == 0:
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=lM.status('playing')))
        elif r == 1:    
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=lM.status('watching')))
        
    
    @client.event
    async def on_ready(self):
        print('Logged on as', self.user, 'on discord version', discord.__version__)
        firstStatus = random.choice(['playing','watching'])
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=lM.status(firstStatus)))
        await self.status_change.start()
                
        
    @client.event
    async def on_message(self, message):
        m = message.content.lower()
        channel = message.channel
        authID = message.author.id
        guild = str(message.guild.id)
        authorizedUsers = ['341767947309678603', '831180756562608159']
        
        if message.author.id == (self.user.id or testid):   #Bot will not reply to itself, on top so nothing will mess with it
            return
        if 'vent' in channel.name.lower(): #Will not reply to any message if the channel has vent in it
            return
        if testing:
            if m == 'ping':                    #Test message to ensure its reciving
                await message.reply('pong')
                
                
        #Whole premise of the bot
        if 'creeper' in m:
            guild = str(message.guild.id)
            uid = str(authID)
            creepers = m.count('creeper')
            chance = random.randint(1, 100)
            guildNameFormatted = message.guild.name.encode('ASCII', 'ignore').decode()
            stat = stats.updateStat(guild, uid, creepers)
            if chance != 2:
               #Random chance creeper
                await message.reply(f'aw man\n'*int(creepers))
                print("Replied to", message.author.name, f"They've done this {stat} times in", guildNameFormatted)
            else:
                rareMessage = random.choice(lM.rareResponses)
                await message.reply(rareMessage)
                print("Replied to", message.author.name, f"They've done this {stat} times in {guildNameFormatted} and they got a rare message!")
                stats.updateStat(guild, uid, int(creepers)*3)
            role = discord.utils.get(message.guild.roles, name='CreeperNotifs')
            try:
                if role not in message.author.roles:
                    await message.author.add_roles(role)
                    print(f'Gave role to {message.author}')
            except AttributeError:
                print(f'{guildNameFormatted} does not have role CreeperNotifs, Role was not given to {message.author}')
                try:
                    await message.guild.create_role(name='CreeperNotifs', color = discord.Color.green())
                    print (f'Created CreeperNotifs in {guildNameFormatted}')
                except Exception as e: print(e)
            except discord.errors.Forbidden:
                print(f'Forbidden to give role to {message.author}')
            except Exception as e: print(e)        
            
            
        if '!stats' in m:                   #Statistics
            if m == '!stats all':
                allStats = stats.getAllStats(guild)
                response = ''
                for each in allStats.keys():
                    line = f'<@{each}> has said creeper {allStats[each]} times\n'
                    response = response + line 
                await message.reply(response)
                return
            if m.startswith('!stats reset'):
                if str(message.author.id) in authorizedUsers:
                    if message.mentions == []:
                        await message.reply('Mention a user shitass')
                        return
                    for uids in message.mentions:
                        if uids.id == '341767947309678603':
                            await message.reply('Nah fuck you')
                        else:
                            stats.resetStat(guild, str(uids.id))
                            await message.reply(f'Stats for <@{uids.id}> have been reset')
                    return
                else: 
                    await message.reply('You do not have permission to do this, ping Void because he\'s the only one with permission')
                    return
            if m == '!stats reset all':
                await message.reply('Confirm in console')
                if stats.resetAll(guild):
                   await message.reply('All stats for this server have been reset')
                   return
                else:
                   await message.reply('Stats have not been reset')
                   return  
            if not bool(message.mentions):
                v = stats.getStat(guild, str(message.author.id))
                if v == (None or 0):
                    await message.reply(f"<@{uid}> hasn't said creeper yet")
                    return
                elif (v <= 500):
                    await message.reply( f'You have said creeper {v} times')
                    return
                else:
                    await message.reply( f'You have said creeper {v} times, you have a problem.\n Please seek medical attention.')
                    return
            else:
                for uids in message.mentions:
                    v = stats.getStat(guild, str(uids.id))
                if v == (None or 0):
                    await message.reply(f"<@{uid}> hasn't said creeper yet")
                    return
                elif (v <= 500):
                    await message.reply( f'You have said creeper {v} times')
                    return
                else:
                    await message.reply( f'You have said creeper {v} times, you have a problem.\nPlease seek medical attention.')
                    return
                    
        
                
#Start Logging
handler = logging.FileHandler(filename=path.join(Path(__file__).parent.absolute(), 'discord.log'), encoding='utf-8', mode='w')


#Start Bot
client = MyClient(intents=intents)
client.run(token, log_handler=handler, log_level=logging.INFO)