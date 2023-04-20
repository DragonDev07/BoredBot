import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from pytube import YouTube
import os

class Media(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    # Log that this cog was loaded
    @commands.Cog.listener()
    async def on_ready(self):
        print("The 'Media' cog has been loaded")

    @commands.hybrid_command()
    async def join(self, ctx):
        if(ctx.author.voice):
            channel = ctx.message.author.voice.channel
            await channel.connect()
            await ctx.send("Joined VC, Use >play or /play to play music")
        else:
            await ctx.send("You must be in a voice channel to run this command!")
        print(f"The 'join' command was run by {ctx.message.author}")
    
    @commands.hybrid_command()
    async def leave(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if (ctx.voice_client):
            await ctx.guild.voice_client.disconnect()
            await ctx.send("Left VC")
        else:
            await ctx.send("I am not in a VC at the moment. Use >join or /join to add me to one!")
        print(f"The 'leave' command was run by {ctx.message.author}")
    
    @commands.hybrid_command()
    async def pause(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if (voice.is_playing()):
            voice.pause()
            await ctx.send("Paused audio")
        else:
            await ctx.send("I am not playing anything at the moment")
        print(f"The 'pause' command was run by {ctx.message.author}")

    @commands.hybrid_command()
    async def resume(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if (voice.is_paused()):
            voice.resume()
            await ctx.send("Resumed Audio")
        else:
            await ctx.send("No audio is paused at the moment!")
        print(f"The 'resume' command was run by {ctx.message.author}")
 
    @commands.hybrid_command()
    async def play(self, ctx, url):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        guild = ctx.message.guild

        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        stream.download(output_path="tmp", filename="temp_audio.mp3")

        path = "tmp/temp_audio.mp3"

        voice.play(discord.FFmpegPCMAudio(path), after=lambda x: end_song(guild, path))
        voice.source = discord.PCMVolumeTransformer(voice.source, 1)

        await ctx.send(f'**Playing: **{url}')
        print(f"The 'play' command was run by {ctx.message.author}, playing video {url}")
    
    @commands.hybrid_command()
    async def stop(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        voice.pause()
        end_song()
        await ctx.send("Stopped Playing Song.")
        print(f"The 'stop' command was run by {ctx.message.author}")

    @commands.hybrid_command()
    async def volume(self, ctx, percent: float=None):
        # Get the voice client for the current guild
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if(not voice):
            await ctx.send("I'm not connected to a voice channel.")
            return
        elif(not voice.is_playing()):
            await ctx.send("I'm not currently playing anything.")
            return
        
        if(percent==None):
            await ctx.send(f"The current volume is {voice.source.volume * 100}%")
        else:
            voice.source.volume = percent / 100
            await ctx.send(f"Volume set to {percent}%.")
        print(f"The 'volume' command was run by {ctx.message.author} to set the volume to {percent}%")

async def setup(client):
    await client.add_cog(Media(client))

def end_song(guild, path):
    os.remove(path)