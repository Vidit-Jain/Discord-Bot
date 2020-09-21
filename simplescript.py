import os

import discord
from discord.ext import commands

import random
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
client = discord.Client()

bot = commands.Bot(command_prefix = '!')


def selfIdentify(message,name):
    f = open("realNames.txt","a+")
    f.write(f'{message.author.id} = {name}\n')
    f.close()


async def findName(message, m):
    f = open("realNames.txt", "r+")
    f1 = f.readlines()
    for x in f1:
        arr = x.split(" = ", 1)
        if str(m.id) == arr[0]:
            await message.channel.send(arr[1])
            break

@bot.event
async def on_ready():
    print ('Bot is ready')


@bot.event
async def on_member_join(member):
    print(f'{member} has joined a server')


@bot.event
async def on_member_remove(member):
    print(f'{member} has left the server')


@bot.command()
async def ping(context):
    await context.send(f'{round(bot.latency * 1000)}ms')


@bot.command(aliases = ['8ball'])
async def _8ball(context, *, q):
    res = list(open('8ballResponses.txt', 'r').readlines())
    await context.send(f'Question: {q}\nAnswer: {random.choice(res)}')


@bot.command(aliases = ['remove'])
async def clear(ctx, amt = 10):
    await ctx.channel.purge(limit=amt+1)


@bot.command()
async def selfidentify(ctx, *, name):
    selfIdentify(ctx,name)
    await ctx.send(f'<@{ctx.author.id}> , you are identified as {name}')


@bot.command()
async def identify(ctx):
    m = ctx.message.mentions
    await findName(ctx.message,m[0])

bot.run(TOKEN)
