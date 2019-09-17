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

for cog in os.listdir("cogs"):
    if cog.endswith(".py"):
        try:
            cog = f"cogs.{cog.replace('.py', '')}"
            bot.add_cog(cog)
        except Exception as e:
            print(f"(cog) can not be loaded:")
            raise e
