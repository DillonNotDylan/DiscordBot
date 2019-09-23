import os
import discord
from discord.ext import commands

''' ^^^^^ Preliminary setup ^^^^^ '''

bot = commands.Bot(command_prefix='.')

class ExampleCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Print a message to the terminal when BeeBoop is ready to go
    @commands.Cog.listener()
    async def on_ready(self):
        print('EXAAAAAAAMPLE')

    # A command pinging BeeBoop. BeeBoop Will respond if connected correctly
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')

def setup(bot):
    bot.add_cog(ExampleCog(bot))










