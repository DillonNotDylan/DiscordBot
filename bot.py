import os
import json
import discord
import youtube_dl
import sys, traceback
from typing import Union
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import Bot

''' ^^^^^ Preliminary setup ^^^^^ '''

# Reading the text file with information of which discord server to connect to
def read_token():
    with open("TheShackToken.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()
players = {}
bot = discord.Client()
# client: Union[Bot, Bot, Bot] = commands.Bot(command_prefix='.')
client = commands.Bot(command_prefix='.')

# initial bot message
@client.event
async def on_ready():
    print(f"{client.user} is ready to go!")


# initial bot message
@client.event
async def on_connect():
    print(f"We're ready to go!")


# tracking joining members
@client.event
async def on_member_join(member):
    print(f"{member} has joined the chat!")
    with open('members.json', 'r') as f:
        members = json.load(f)

    await update_data(members, member)

    with open('members.json', 'w') as f:
        json.dump(members, f)


# tracking departing members
@client.event
async def on_member_remove(member):
    print(f"{member} has left the chat!")


# tracking messages
@client.event
async def on_message(self, message):
    if message.author == self.bot.users:
        return

    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
    await client.process_commands(message)

    with open('members.json', 'r') as f:
        members = json.load(f)

    await update_data(members, message.author)
    await add_xp(members, message.author, 100)
    await level_up(members, message.author, message.channel)

    with open('members.json', 'w') as f:
        json.dump(members, f)

async def update_data(members, member):
    if not member.id in members:
        members[member.id] = {}
        members[member.id]['experience'] = 0
        members[member.id]['level'] = 1

async def add_xp(members, member, xp):
    members[member.id]['experience'] += xp

async def level_up(members, member, channel):
    experience = members[member.id]['experience']
    current_level = members[member.id]['level']
    next_level = int(experience ** (1/4))

    if current_level < next_level:
        await ctx.send(channel, '{} has leveled up to level {}'.format(member.mention, next_level))
        members[member.id]['level'] = next_level




# ping test to make sure bot is connected
@client.command()
async def ping(ctx):
    await ctx.send('Pong!')


# connect the bot to the chat
@client.command(pass_context=True)
async def connect(ctx):
    channel = ctx.message.author.voice.channel
    await ctx.send('Use the dot operator to access commands ^_^')
    await ctx.send("\tExample: Try (.commands) to access a list of commands")
    await channel.connect()


# disconnect the bot from the chat
@client.command()
async def disconnect(ctx):
    server = ctx.message.guild
    voice = server.voice_client
    await voice.disconnect()


# Displays the currently playing song.
@client.command()
async def now(self, ctx: commands.Context):
    await ctx.send(embed=ctx.voice_state.current.create_embed())


# pause the current music
@client.command()
async def pause(ctx):
    server = ctx.message.guild
    voice = server.voice_client
    await ctx.message.add_reaction('pausing ⏯')
    voice.pause()


# resume playing the currently queued song
@client.command()
async def resume(ctx):
    server = ctx.message.guild
    voice = server.voice_client
    await ctx.message.add_reaction('resuming ⏯')
    voice.resume()


@client.command()
async def commands(ctx):
    await ctx.send('Use the dot operator to access commands ^_^')
    await ctx.send('\t.connect            - allows Bot to join the current voice chat')
    await ctx.send('\t.disconnect         - removes Bot from the current voice chat')
    await ctx.send("\t.play 'YouTube URL' - queue a song for the current voice chat")
    await ctx.send('\t.pause              - pause the music being played in voice chat')
    await ctx.send('\t.resume             - begin playing the song currently queued')


# attempts to play a song from a YouTube URL
@client.command(pass_context=True, brief="This will play a song 'play [url]'", aliases=['pl'])
async def play(ctx, url: str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")

    except PermissionError:
        await ctx.send("Wait for the current playing music end or use the 'stop' command")
        return

    await ctx.send("Getting everything ready, playing audio soon")

    print("Someone wants to play music let me get that ready for them...")

    voice = get(client.voice_clients, guild=ctx.guild)


    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors':
            [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, 'song.mp3')

    voice.play(discord.FFmpegPCMAudio("song.mp3"))
    voice.volume = 100
    voice.is_playing()


extensions = ['', '', '']


for extension in extensions:
    client.load_extension(extensions)


'''
for cog in os.listdir("cogs"):
    if cog.endswith(".py"):
        try:
            cog = f"cogs.{cog.replace('.py', '')}"
            bot.load_extension(extension)
        except Exception as e:
            print(f"(cog) can not be loaded:")
            raise e
'''
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


client.run(token)
