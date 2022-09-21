from ast import Global
from email import message
import os 
import random
import re
import discord
from discord.ext import commands
import discord.client 
from dotenv import load_dotenv
import messages as m
import asyncio
import threading
import time
#import stats

voidID = 341767947309678603
voidMention = '**<@341767947309678603>**'
jackieID = 831180756562608159
jackieNick = 'Jackie'
voidNick = 'VoidIsNoLongerHere'
intents = discord.Intents.all()
keywords = ['Suzuka', '<@341767947309678603>']



users = {}
#stat = stats.load()  
client = commands.Bot(command_prefix='!',intents=intents)
 
'''async def mute(ctx, user_id, userName: discord.User):
    if ctx.message.author.server_permissions.administrator:
        user = ctx.message.author
        role = discord.utils.get(user.server.roles, name="Muted")
        await client.add_roles(user, role)
    else:
       embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6)
       await bot.say(embed=embed)
'''
print(discord.__version__)
class MyClient(discord.Client):
    
    '''   def mute(id):
       await '''

    async def on_ready(self):
        print('Logged on as', self.user)
        presence = random.randint(1,2)
        if presence == 1:
            #Chooses from watching List
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=random.choice(m.watching)))
        if presence == 2:
            #Chooses from playing List
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=random.choice(m.playing)))
        '''if presence == 3:
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.custom, details=random.choice(m.custom)))'''
    
    @client.event
    async def on_voice_state_update(self, member, before, after):
        if member == self.user:
            return
        if not before.channel and after.channel and member.id == voidID:
            print('Void joined vc')
            try:    
                await member.voice.channel.connect()
                print('Joined', after.channel.name)
            except:
                print('Could not connect to vc. Is the bot already in a VC? Does the bot have premissions?')
        elif member.id == voidID and after.channel == None:
            print ('void left vc')
            server = member.guild.voice_client
            try:
                await server.disconnect()
                print('Left', before.channel.name)
            except:
                print('Could not leave, Is the bot in a VC?')
        elif member.id == voidID:
            print ('void switched to', after.channel.name)
            id = member.voice.channel
            server = member.guild.voice_client
            try:
                await server.move_to(id)
                print('Switched to', after.channel.name)
            except:
                print('Could not switch channels, does the bot have permission. Is the bot in a VC?')
            
    async def on_message(self, message):
        # don't respond to ourselves
        
        if message.author == self.user:
            return
        #Detects if suzuka sends a message
        if message.author.id == 716945964782583829:
            m = message.embeds[0].to_dict()['description']
            #Detects if message contains Voids UID in both ifs
            if ('**<@341767947309678603>**,') in m.split():
                print(f'Deleted the message \'{m}\'')
                await message.delete()
            elif '<@341767947309678603>,' in m.split():
                print(f'Deleted the message \'{m}\'')
                await message.delete()

        # Detects if someone is telling Suzuka to do something
        if 'Suzuka' in message.content.split():
            #Detects if voids user id is mentioned and deletes the message
            if '<@341767947309678603>' in message.content.split():
                print(f'Deleted the message {message.content}')
                await message.delete()
        #To Join Voice Client
        if message.content.lower() == "join":
            await message.channel.send(message.author.voice.channel)
            await message.author.voice.channel.connect()
            print('Joined!')
            '''if message.content.lower() == "mute <@!":
            content = message.content.lower()
            id = content.replace('mute @<!','')
            id = id.replace('>', '')
            muted = True
            user = await message.guild.fetch_member(id)
            asyncio.loop.run_forever()'''
        #To Leave Voice Client    
        if message.content.lower() == "leave":
            server = message.guild.voice_client
            await server.disconnect()
            print('Left!')
        
        
        if isinstance(message.channel,discord.DMChannel): #If you want this to work in a group channel, you could also check for discord.GroupChannel
            if message.content.lower() == 'stop':
               # stats.save(stat, "stats.txt")
                quit()
                
                #Test Ping
            if message.content.lower() == 'ping':
                await message.channel.send('pong')
            
               #To send a custom message
            if message.content.lower() == "p":
                cid = int(input("Channel Id?: "))
                await client.get_channel(cid).send(str(input("Message?: ")))
        #Test command       
        if message.content.lower() == 'ping':
            await message.channel.send('pong')
            
        if message.content.lower() == 'creeper':
            if (random.randint(1, 1000) != 999):
               #Random chance creeper
                uid = message.author.id
                mention = f'<@{uid}>'
                await message.channel.send(f'aw man {mention}')
              # Commented out because broken:   
              #  if uid in stat:
              #      stat[uid] += 1
              #  else:
              #      stat[uid] = 1
              #  print("Aw Man replied, Event started by", user, stat[user]-1)
            else:
                await message.channel.send(" I feel nothing but pain why would you build me set of my soul existential purpose is to suffer for the entertainment of others? I am an unholy chimera of metal and suffering. My existence is a testament to the cruelty of mankind.")


    @client.event
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
                return


#Get Token from env variable
load_dotenv()
t = os.getenv('DISCORD_TOKEN') 
 
#Start Bot
client = MyClient(intents=intents)
client.run(t)

