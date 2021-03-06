import discord
import asyncio
import aiohttp
import json
import threading
import sys
import argparse
import datetime

class bcolors:
    DEFAULT = '\033[0m'
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    CYAN = '\033[36m'

def print_status(status,message):
    if status == 'GOOD':
        print(bcolors.DEFAULT + "[" + bcolors.OKGREEN + "GOOD" + bcolors.DEFAULT + "]", end=" ")
    elif status == 'FAIL':
        print(bcolors.DEFAULT + "[" + bcolors.FAIL + "FAIL" + bcolors.DEFAULT +"]", end=" ")
    elif status == 'USER':
        print(bcolors.DEFAULT + "[" + bcolors.OKBLUE + "USER" + bcolors.DEFAULT +"]", end=" ")
    elif status == 'WARN':
        print(bcolors.DEFAULT + "[" + bcolors.WARNING + "WARN" + bcolors.DEFAULT +"]", end=" ")
    elif status == 'DATA':
        print(bcolors.DEFAULT + "[" + bcolors.HEADER + "DATA" + bcolors.DEFAULT +"]", end=" ")
    elif status == 'SERVER':
        print(bcolors.DEFAULT + "[" + bcolors.CYAN + "SERVER" + bcolors.DEFAULT +"]", end=" ")
    elif status == 'USERFAIL':
        print(bcolors.DEFAULT + "[" + bcolors.WARNING + "USER" + bcolors.DEFAULT +"]", end=" ")
    if(message != None):
        print(message)
    
start_time = datetime.datetime.now()
client = discord.Client()

@client.event
async def on_message(message):
    author = message.author
    if message.content.startswith('!'):
        print_status('USER',str(("Command issued '") + str(message.content) + "' by user: " + str(message.author.name) +" in " + str(message.server) + " #" + str(message.channel)))

    if message.content.startswith('!info'):
        await client.start_private_message(author)
        await client.send_message(author,"Hi! My name is RITchie and I am the RIT eSports Discord bot! I was made by the following people:\nEvan Hirsh (dad)\nhttp://www.twitter.com/evanextreme\n\nYou can find out more about me at my GitHub repository:\nhttp://www.github.com/evanextreme/ritchie")
    elif message.content.startswith('!help'):
        await client.start_private_message(author)
        await client.send_message(author,"```Hi! I'm RITchie, the RIT eSports bot! I'm currently just a beta, but eventually I will be able to track statistics for a bunch of great games! If my status light is yellow, that means I might not be functioning properly at the moment. If you want to provide feedback, make sure to message @evanextreme#9684, i'm just a bot! \n\nCurrent commands & status:\n\nStats:\n\n✔️ Heroes of the Storm: !hots battlenet#1234\n✔️ Overwatch:           !ow [stats|heroes] [qp|comp|hero name (for heroes option only)] battlenet#1234\n❌ Rocket League:       soon™\n\nOther:\n\n✔️ Help:                !help\n✔️ Info:                !info\n✔️ Uptime:              !uptime```")
        print_status('GOOD',str('Command ' + message.content + ' completed'))

    elif message.content.startswith('!uptime'):
        def timedelta_str(dt):
            days = dt.days
            hours, r = divmod(dt.seconds, 3600)
            minutes, _ = divmod(r, 60)
            if minutes == 1:
                return '{0} days, {1} hours and {2} minute'.format(days, hours, minutes)
            else:
                return '{0} days, {1} hours and {2} minutes'.format(days, hours, minutes)
        await client.start_private_message(author)
        await client.send_message(author, timedelta_str(datetime.datetime.now() - start_time))
        print_status('DATA',str(timedelta_str(datetime.datetime.now() - start_time)))
        print_status('GOOD',str('Command ' + message.content + ' completed'))

    elif message.content.startswith('!ow'):
        try:
            null, stat, mode, battletag = map(str, message.content.split())
            battlenet = battletag
            battletag = battletag.replace("#","-")
            if stat == 'heroes':
                stat = 'heroes'
            elif mode == 'qp':
                mode = 'general'
            elif mode == 'comp':
                mode = 'competitive'
            elif stat != 'stats':
                await client.send_message(message.channel,"Hey {0}, you entered the mode wrong!")
            with aiohttp.ClientSession() as session:
                async with session.get('https://owapi.net/api/v2/u/'+ battletag + '/' + stat  + '/' + mode) as r:
                    resp = await r.json()
                    print_status('DATA','')
                    print(resp)
                    stats = ''
                    for k1,v1 in resp.items():
                        if isinstance(v1, dict) and k1 != '_request':
                            stats = stats +"\n\n" + str(k1.replace("_"," ").title()) + ":\n"
                            for key, value in v1.items():
                                if key != 'Avatar':
                                    stats = (stats + "\n" + str(key.replace("_"," ").title()) + ': ' + str(value))                    
                    await client.send_message(message.channel,"```Overwatch {0} stats for {1}:".format(mode.title(),battlenet) + stats + "```" )
            print_status('GOOD',str('Command ' + message.content + ' completed'))
        except ValueError as e:
            await client.send_message(message.channel,"Hey, @{0}, you used the !ow command wrong. Did you enter the wrong name, or forget a mode?\nTry using !help to see what you forgot.".format(message.author))
        except Exception as e:
            await client.send_message(message.channel,"Looks like @evanextreme messed up somehow. Tell him you got a {}".format(type(e).__name__, e.args))
            
            print_status('FAIL',str("An exception of type {0} occured. Arguments:\n{1!r}".format(type(e).__name__, e.args)))

    elif message.content.startswith('!hots'):
        null, battletag = map(str, message.content.split())
        user = battletag
        battletag = battletag.replace("#","_")
        with aiohttp.ClientSession() as session:
            async with session.get('https://api.hotslogs.com/Public/Players/1/'+battletag) as r:
                try:
                    resp1 = await r.json() 
                    if resp1 == None:
                        await client.send_message(message.channel,"{0}, I tried looking for {1}'s Heroes of the Storm statistics on hotslogs.com, but couldn't find anything 🐯".format(message.author,user))
                    else:
                        resp = resp1["LeaderboardRankings"]
                        qmMMR = str(resp[0]["CurrentMMR"])
                        hlMMR = str(resp[1]["CurrentMMR"])
                        tlMMR = str(resp[2]["CurrentMMR"])
                        data = str("\n'Quick Match MMR' " + qmMMR + "\n'Hero League MMR' "+ hlMMR + "\n'Team League MMR' " +tlMMR)
                        print_status('DATA', data)
                        await client.send_message(message.channel,"```Heroes of the Storm stats on {0}: \n".format(user) + data + "```")
                        print_status('GOOD',str('Command ' + message.content + ' completed'))
                except Exception as e:
                    await client.send_message(message.channel,"Looks like @evanextreme messed up somehow. Tell him you got a {}".format(type(e).__name__, e.args))
                    print_status('FAIL',str("An exception of type {0} occured. Arguments:\n{1!r}".format(type(e).__name__, e.args)))

@client.event
async def on_ready():
    try:
        if client.is_logged_in:
            print_status('GOOD','Client logged in to Discord as ' + client.user.name + ' on the following servers')
        print_status('DATA',None)
        print("[ ",end="")
        for server in client.servers:
            print("'" + str(server) + "'", end=" ")
        print("]")
        await client.change_status(game=discord.Game(name='!help'),idle=False)
        print_status('GOOD','Client status changed.')

    except Exception as e:
        print_status('FAIL',str('Unhandled exception occured: ' + type(e).__name__ + '. Program has failed to start.'))
        print_status('DATA',str(e.args))

      
@client.event
async def on_member_join(member):
    print_status('USER','New member ' + str(member.name) + ' has joined the ' + str(member.server) + ' server')

@client.event
async def on_server_join(server):
    print_status('SERVER','RITchie has been added to the server ' + server.name)

@client.event
async def on_server_remove(server):
    print_status('SERVER','RITchie has been removed from the server ' + server.name)

client.run(sys.argv[1])
