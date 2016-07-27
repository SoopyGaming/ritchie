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
                rank = int(resp["data"]["competitive"]["rank"])
                print("Rank: " + str(rank))
 
client.run('MjAzOTEwMzU5NjA0NTI3MTA1.Cnqz3A.T7itPbqf4FaqsxW65ZZq8yitQRk')