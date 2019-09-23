import os
import discord
from discord.ext import commands

''' ^^^^^ Preliminary setup ^^^^^ '''

bot = commands.Bot(command_prefix='.')

class ExampleCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('The cogs are working!')


    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')


    # initial bot message
    @commands.Cog.listener()
    async def on_connect(self):
        print(f"We're ready to go!")


    # tracking joining members
    @commands.Cog.listener()
    async def on_member_join(member):
        print(f"{member} has joined the chat!")


    # tracking departing members
    @commands.Cog.listener()
    async def on_member_remove(member):
        print(f"{member} has left the chat!")


    # tracking messages
    @commands.Cog.listener()
    async def on_message(self, message):
        print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")


def setup(bot):
    bot.add_cog(ExampleCog(bot))
































'''Shit to add later'''

    #     @commands.command(name='stop')
    #     @commands.has_permissions(manage_guild=True)
    #     async def _stop(self, ctx: commands.Context):
    #         """Stops playing song and clears the queue."""
    #
    #         ctx.voice_state.songs.clear()
    #
    #         if not ctx.voice_state.is_playing:
    #             ctx.voice_state.voice.stop()
    #             await ctx.message.add_reaction('⏹')
    #
    #     @commands.command(name='skip')
    #     async def _skip(self, ctx: commands.Context):
    #         """Vote to skip a song. The requester can automatically skip.
    #         3 skip votes are needed for the song to be skipped.
    #         """
    #
    #         if not ctx.voice_state.is_playing:
    #             return await ctx.send('Not playing any music right now...')
    #
    #         voter = ctx.message.author
    #         if voter == ctx.voice_state.current.requester:
    #             await ctx.message.add_reaction('⏭')
    #             ctx.voice_state.skip()
    #
    #         elif voter.id not in ctx.voice_state.skip_votes:
    #             ctx.voice_state.skip_votes.add(voter.id)
    #             total_votes = len(ctx.voice_state.skip_votes)
    #
    #             if total_votes >= 3:
    #                 await ctx.message.add_reaction('⏭')
    #                 ctx.voice_state.skip()
    #             else:
    #                 await ctx.send('Skip vote added, currently at **{}/3**'.format(total_votes))
    #
    #         else:
    #             await ctx.send('You have already voted to skip this song.')
    # attempts to join the
    # @client.command()
    # async def join(ctx, *, channel: discord.VoiceChannel = None):
    #     if not channel:
    #         try:
    #             channel = ctx.author.voice.channel
    #         except AttributeError:
    #             raise InvalidVoiceChannel('No channel to join. Please either specify a valid channel or join one.')
    #
    #     vc = ctx.voice_client
    #
    #     if vc:
    #         if vc.channel.id == channel.id:
    #             return
    #         try:
    #             await vc.move_to(channel)
    #         except asyncio.TimeoutError:
    #             raise VoiceConnectionError(f'Moving to channel: <{channel}> timed out.')
    #     else:
    #         try:
    #             await channel.connect()
    #         except asyncio.TimeoutError:
    #             raise VoiceConnectionError(f'Connecting to channel: <{channel}> timed out.')
    #
    #     await ctx.send(f'Connected to: **{channel}**', delete_after=20)