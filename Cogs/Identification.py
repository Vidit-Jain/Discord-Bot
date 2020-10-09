import discord
from discord.ext import commands
import os


class Identification(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def checkName(self, author):
        'Returns true if the name is already present in the list, else returns false'

        with open("Resources/realNames.txt", "r") as f:
            for person in f:
                if str(author.id) == tuple(person.split(" = ", 1))[0]:
                    return True
        return False

        
    def selfIdentify(self, _id, name):
        'Adds the name to the list'

        with open("Resources/realNames.txt", "a+") as f:
            f.write(f'{_id} = {name}\n')


    def findName(self, person):
        'Gets the identified name of the mentioned user'

        with open("Resources/realNames.txt", "r+") as f:
            for entry in f:
                _id, name = entry.split(" = ", 1)
                if str(person.id) == _id:
                    return name
        return "not found\n"


    def removeName(self, userId):
        'To remove the identity of the user'

        isPresent = False
        with open("Resources/realNames.txt", 'r') as f:
            with open("Resources/temp.txt", 'w') as fout:
                for person in f:
                    if (str(userId)) == person.split(' = ', 1)[0]:
                        isPresent = True
                    else:
                        fout.write(person)
        if (isPresent):
            os.remove('Resources/realNames.txt')
            os.rename('Resources/temp.txt', 'Resources/realNames.txt')
            return "you are removed"

        return "your identity doesn't exist"


    def reidentify(self, _id, name):
        self.removeName(_id)
        self.selfIdentify(_id, name)


    @commands.command(aliases=['selfid', 'sid'])
    async def selfidentify(self, ctx, *, name):
        '!selfidentify <Your name>'

        author = ctx.author
        if self.checkName(author):
            self.reidentify(author.id, name)
            await ctx.send(f'<@{author.id}> your identity has been updated to {name}')
            return

        self.selfIdentify(author.id, name)
        await ctx.send(f'<@{author.id}>, you are identified as {name}!')


    @commands.command(aliases=['id'])
    async def identify(self, ctx):
        '!identify @handle'

        ans = ''

        for person in ctx.message.mentions:
            ans += f'{person} is {self.findName(person)}'
        await ctx.send(ans)


    @commands.command(aliases=['removeid', 'rid'])
    async def removeidentity(self, ctx):
        '!removeidentity'

        _id = ctx.author.id
        await ctx.send(f'{ctx.author} {self.removeName(_id)}')


def setup(bot):
    bot.add_cog(Identification(bot))