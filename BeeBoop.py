### BeepBoop is an original Discord Bot made by Dillon Burns###

import os
import json
import discord
import youtube_dl
from discord.utils import get
from discord.ext import commands, tasks
''' ^^^^^ Preliminary setup ^^^^^ '''


# Reading the text file with information of which discord server to connect to
def read_token():
    with open("TheShackToken.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


# Initialize some important variables
token = read_token()
client = commands.Bot(command_prefix='.')


# Tracking messages and processing commands
@client.event
async def on_message(message):
    await client.process_commands(message)


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


# pause the current music
@client.command()
async def pause(ctx):
    server = ctx.message.guild
    voice = server.voice_client
    #await ctx.message.add_reaction('pausing ⏯')
    voice.pause()


# resume playing the currently queued song
@client.command()
async def resume(ctx):
    server = ctx.message.guild
    voice = server.voice_client
    await ctx.message.add_reaction('resuming ⏯')
    voice.resume()


# attempts to play a song from a YouTube URL
@client.command(pass_context=True, brief="This will play a song 'play [url]'", aliases=['pl'])
async def play(ctx, url: str):
    song_exists = os.path.isfile("song.mp3")
    try:
        if song_exists:
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


# Loading our Cogs
extensions = ['cogs.server', 'cogs.example']
for e in extensions:
    client.load_extension(e)


# Starting our Bot
client.run(token)