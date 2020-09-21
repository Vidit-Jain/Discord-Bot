import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(f'{guild.name} has been connected to the bot')
@client.event
async def on_message(message):
    if message.content == "!hi":
        await message.channel.send("Sup dude")
client.run(TOKEN)