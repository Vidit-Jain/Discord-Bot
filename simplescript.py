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


def checkName(author):
    'Returns true if the name is already present in the list, else returns false'

    with open("realNames.txt", "r") as f:
        for person in f:
            _id, name = tuple(person.split(" = ", 1))
            if str(author.id) == _id:
                return True
    return False


def selfIdentify(_id, name):
    'Adds the name to the list'

    with open("realNames.txt", "a+") as f:
        f.write(f'{_id} = {name}\n')


def findName(person):
    'Gets the identified name of the mentioned user'

    with open("realNames.txt", "r+") as f:
        for entry in f:
            _id, name = entry.split(" = ", 1)
            if str(person.id) == _id:
                return name
    return "not found\n"


def removeName(userId):
    'To remove the identity of the user'

    isPresent = False
    with open("realNames.txt", 'r') as f:
        with open("temp.txt", 'w') as fout:
            for person in f:
                _id, name = person.split(' = ', 1)
                if (str(userId)) == _id:
                    isPresent = True
                else:
                    fout.write(person)
    if (isPresent):
        os.remove('realNames.txt')
        os.rename('temp.txt', 'realNames.txt')
        return "you are removed"

    return "your identity doesn't exist"


def reidentify(_id, name):
    removeName(_id)
    selfIdentify(_id, name)


async def parentErrorHandler(ctx):
    f = open("errorResponses.txt", "r")
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


@bot.command(aliases=['remove'])
async def clear(ctx, amt=10):
    '!clear <no-of-messages>'

    await ctx.channel.purge(limit=amt + 1)


@bot.command(aliases=['selfid', 'sid'])
async def selfidentify(ctx, *, name):
    '!selfidentify <Your name>'

    author = ctx.author
    if checkName(author):
        reidentify(author.id, name)
        await ctx.send(f'<@{author.id}> your identity has been updated to {name}')
        return

    selfIdentify(author.id, name)
    await ctx.send(f'<@{author.id}>, you are identified as {name}!')


@bot.command(aliases=['id'])
async def identify(ctx):
    '!identify @handle'
    ans = ''
    if len(ctx.message.mentions) == 0:
        await parentErrorHandler(ctx)
    else:
        for person in ctx.message.mentions:
            ans += f'{person} is {findName(person)}'
        await ctx.send(ans)


@bot.command(aliases=['removeid', 'rid'])
async def removeidentity(ctx):
    '!removeidentity'
    _id = ctx.author.id
    await ctx.send(f'{ctx.author} {removeName(_id)}')


bot.run(TOKEN)