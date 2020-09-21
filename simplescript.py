import os

import discord
from discord.ext import commands

import random
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
        
@client.command()
async def ping(context):
    await context.send(f'{round(bot.latency * 1000)}ms')

@client.command(aliases = ['8ball'])
async def _8ball(context, *, q):
    res = list(open('8ballResponses.txt', 'r').readlines())
    await context.send(f'Question: {q}\nAnswer: {random.choice(res)}')

@client.command(aliases = ['remove'])
async def clear(ctx, amt = 10):
    await ctx.channel.purge(limit=amt+1)

@client.command()
async def selfidentify(ctx, *, name):
    await ctx.send(f'{ctx.author}, you are identified as {name}')
        
client.run(TOKEN)
