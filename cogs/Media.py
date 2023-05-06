import discord
from discord.ext import commands
from discord import app_commands
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

    # Propagate the error to the global error handler
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await self.bot.on_command_error(ctx, error)

    # Command that makes the bot join the vc
    @app_commands.command()
    async def join(self, interaction: discord.Interaction):
        if(interaction.user.voice):
            channel = interaction.user.voice.channel
            await channel.connect()
            embed = discord.Embed(title="Joined!", description = "Joined VC, Use /play to play music/videos", colour = discord.Colour.blurple())
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title="Error", description = "You must be in a voice channel to run this command!", colour = discord.Colour.red())
            await interaction.response.send_message(embed=embed)
        print(f"The 'join' command was run by {interaction.user}")
    
    # Command that makes the bot leave the vc
    @app_commands.command()
    async def leave(self, interaction: discord.Interaction):
        voice = discord.utils.get(self.client.voice_clients, guild=interaction.guild)
        if (voice):
            await interaction.guild.voice_client.disconnect()
            embed = discord.Embed(title = "Left!", description="Left VC, use /join to add me back", colour = discord.Colour.blurple())
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title = "Couldn't Leave", description="I am not in a VC at the moment. Use /join to add me to one!", colour = discord.Colour.red())
            await interaction.response.send_message(embed=embed)
        print(f"The 'leave' command was run by {interaction.user}")
    
    # Command that pauses the current playing audio
    @app_commands.command()
    async def pause(self, interaction: discord.Interaction):
        voice = discord.utils.get(self.client.voice_clients, guild=interaction.guild)
        if (voice.is_playing()):
            voice.pause()
            embed = discord.Embed(title = "Paused", description="Paused Audio, use /resume to resume playing", colour = discord.Colour.blurple())
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title = "Could not Pause!", description="I am not playing anything at the moment", colour = discord.Colour.red())
            await interaction.response.send_message.send(embed=embed)
        print(f"The 'pause' command was run by {interaction.user}")

    # Command that resumes paused audio
    @app_commands.command()
    async def resume(self, interaction: discord.Interaction):
        voice = discord.utils.get(self.client.voice_clients, guild=interaction.guild)
        if (voice.is_paused()):
            voice.resume()
            embed = discord.Embed(title = "Resumed", description="Resumed playing audio", colour = discord.Colour.blurple())
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title = "Couldn't Resume!", description = "No audio is paused at the moment", colour = discord.Colour.red())
            await interaction.response.send_message(embed=embed)
        print(f"The 'resume' command was run by {interaction.user}")
 
    # Command that playes given YouTube URL
    @app_commands.command()
    async def play(self, interaction: discord.Interaction, url: str):
        voice = discord.utils.get(self.client.voice_clients, guild=interaction.guild)
        guild = interaction.guild
        
        await interaction.response.defer()

        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        stream.download(output_path="tmp", filename="temp_audio.mp3")
        
        path = "tmp/temp_audio.mp3"
        voice.play(discord.FFmpegPCMAudio(path), after=lambda x: end_song(guild, path))
        voice.source = discord.PCMVolumeTransformer(voice.source, 1)

        embed = discord.Embed(title = "Now Playing", description = f"{url}", colour = discord.Colour.blurple())
        await interaction.followup.send(embed=embed)
        print(f"The 'play' command was run by {interaction.user}, playing video {url}")
    
    # Command that stops playing audio (delets file, cannot be resumed)
    @app_commands.command()
    async def stop(self, interaction: discord.Interaction):
        voice = discord.utils.get(self.client.voice_clients, guild=interaction.guild)
        guild = interaction.guild
        path = "tmp/temp_audio.mp3"
        voice.pause()
        end_song(guild, path)
        embed = discord.Embed(title = "Stopped", description="Stopped Playing Audio", colour = discord.Colour.blurple())
        await interaction.response.send_message(embed=embed)
        print(f"The 'stop' command was run by {interaction.user}")

    # Command to get or set volume of the audio
    @app_commands.command()
    async def volume(self, interaction: discord.Interaction, percent: float=None):
        # Get the voice client for the current guild
        voice = discord.utils.get(self.client.voice_clients, guild=interaction.guild)
        if(not voice):
            embed = discord.Embed(title = "Error!", description="I'm not connected to a voice channel.", colour = discord.Colour.red())
            await interaction.response.send_message(embed=embed)
            return
        elif(not voice.is_playing()):
            embed = discord.Embed(title = "Error!", description="I'm not currently playing anything.", colour = discord.Colour.red())
            await interaction.response.send_message(embed=embed)
            return

        if(percent==None):
            embed = discord.Embed(title = "Volume", description=f"The current volume is {voice.source.volume * 100}%", colour = discord.Colour.blurple())
            await interaction.response.send_message(embed=embed)
        else:
            voice.source.volume = percent / 100
            embed = discord.Embed(title = "Volume", description=f"Volume set to {percent}%.", colour = discord.Colour.blurple())
            await interaction.response.send_message(embed=embed)
        print(f"The 'volume' command was run by {interaction.user} to set the volume to {percent}%")

async def setup(client):
    await client.add_cog(Media(client))

def end_song(guild, path):
    os.remove(path)