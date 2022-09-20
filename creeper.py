from ast import Global
from email import message
import os 
import random
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
jackieID = 831180756562608159
jackieNick = 'Jackie'
voidNick = 'VoidIsNoLongerHere'
intents = discord.Intents.all()


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
            await member.voice.channel.connect()
            print('Joined', after.channel.name)
        elif member.id == voidID and after.channel == None:
            print ('void left vc')
            server = member.guild.voice_client
            await server.disconnect()
            print('Left', before.channel.name)
        elif member.id == voidID:
            print ('void switched to', after.channel.name)
            id = member.voice.channel
            server = member.guild.voice_client
            await server.move_to(id)
            print('Switched to', after.channel.name)
    
            
    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return
        
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
                
        if message.content.lower() == 'ping':
            await message.channel.send('pong')
        if message.content.lower() == 'creeper':
            if (random.randint(1, 1000) != 999):
               #  user = message.author.name + '#' +message.author.discriminator
                uid = message.author.id
                mention = f'<@{uid}>'
                await message.channel.send(f'aw man {mention}')
                
              #  if uid in stat:
              #      stat[uid] += 1
              #  else:
              #      stat[uid] = 1
              #  print("Aw Man replied, Event started by", user, stat[user]-1)
            else:
                await message.channel.send(" I feel nothing but pain why would you build me set of my soul existential purpose is to suffer for the entertainment of others? I am an unholy chimera of metal and suffering. My existence is a testament to the cruelty of mankind.")


    @client.event
    async def on_member_update(self,before, after):
        
        if before.id == jackieID:
            if before.name != after.name:
                print(f'jackie changed her username: {before.name} was changed to {after.name}')
            elif before.nick != after.nick:
                print(f'jackie\'s nickname: {before.nick} was changed to {after.nick}')
        if after.id == voidID:
            if after.nick != None:
                if after.nick != voidNick:
                    try:
                        print('Detected Name Change to', after.nick)
                        await after.edit(nick = voidNick)
                        print('Fixed')
                    except discord.Forbidden:
                        print(f'Could Not Change Nickname of {after}. Does the bot have Permissions? Are you the server owner?')
                else:
                    return
            else:
                return



load_dotenv()
t = os.getenv('DISCORD_TOKEN')  
client = MyClient(intents=intents)
client.run(t)

