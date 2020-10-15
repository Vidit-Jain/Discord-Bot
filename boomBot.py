import os

import discord
from discord.ext import commands

import random
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix = '!')


async def parentErrorHandler(ctx):
    f = open("Resources/errorResponses.txt", "r")
    f1 = f.readlines()
    await ctx.send(random.choice(f1))

@bot.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.MissingRequiredArgument):
        await parentErrorHandler(ctx)

@bot.event
async def on_ready():
    'Just to show that the bot is online and functioning'

    print('Bot is ready')


@bot.event
async def on_member_join(member):
    'To keep a track of who has entered the server'

    print(f'{member} has joined a server')


@bot.event
async def on_member_remove(member):
    'To keep a track of who has exited the server'

    print(f'{member} has left the server')


@bot.command()
async def ping(context):
    '!ping'

    await context.send(f'{round(bot.latency * 1000)}ms')


@bot.command(aliases=['8ball'])
async def _8ball(context, *, q):
    '!8ball <question>'

    res = list(open('8ballResponses.txt', 'r').readlines())
    await context.send(f'Question: {q}\nAnswer: {random.choice(res)}')

for fileName in os.listdir('./Cogs'):
    if fileName.endswith('.py'):
        bot.load_extension(f'Cogs.{fileName[:-3]}')

bot.run(TOKEN)