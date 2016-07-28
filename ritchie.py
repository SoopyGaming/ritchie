import discord
import asyncio
import aiohttp
import json

client = discord.Client()

@client.event
async def on_message(message):
    if message.content.startswith('!ow'):
        null, battletag = map(str, message.content.split())
        battletag = battletag.replace("#","-")
        with aiohttp.ClientSession() as session:
            async with session.get('https://api.lootbox.eu/pc/us/'+ battletag +'/profile') as r:
                resp = await r.json()
                print(resp)
                rank = int(resp["data"]["competitive"]["rank"])
                print(rank)
                await client.send_message(message.channel,"{}'s Overwatch rank is:! ".format(message.author) + str(rank))



    if message.content.startswith('!hots'):
        null, battletag = map(str, message.content.split())
        battletag = battletag.replace("#","_")
        with aiohttp.ClientSession() as session:
            async with session.get('https://api.hotslogs.com/Public/Players/1/'+battletag) as r:
                resp = await r.json()
                print(resp)
                for resp["CurrentMMR"] in resp:
                	if int(resp["GameMode"]) == "HeroLeague":
                	    rank = int(resp[CurrentMMR])

                #rank = int(resp["LeaderboardRankings"]["CurrentMMR"])
                print(rank)
                await client.send_message(message.channel,"{}'s Overwatch rank is:! ".format(message.author) + str(rank))


client.run('MjA3Mjk0MzM0NDUyNjI5NTA1.CnrVhg.7LytKiF4y3LjL_6h07rmQD820p4')