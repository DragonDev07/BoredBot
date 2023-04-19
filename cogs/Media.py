import discord
from discord.ext import commands
from discord import FFmpegPCMAudio

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
        else:
            await ctx.send("I am not playing anything at the moment")
        print(f"The 'pause' command was run by {ctx.message.author}")

    @commands.hybrid_command()
    async def resume(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if (voice.is_paused()):
            voice.resume()
        else:
            await ctx.send("No audio is paused at the moment!")
        print(f"The 'resume' command was run by {ctx.message.author}")
 
    @commands.hybrid_command()
    async def play(self, ctx, args):
        await ctx.send("This command is still under development, please try again later.")
        # voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        # if (args == "song1"):
        #     source = FFmpegPCMAudio("static_music.mp3")
        #     await ctx.send("Playing music")
        # elif (args == "song2"):
        #     source = FFmpegPCMAudio("static_music.mp3")
        #     await ctx.send("Playing other definitly more different music")
        # player = voice.play(source)
        print(f"The 'play' command has been run by {ctx.message.author}")

async def setup(client):
    await client.add_cog(Media(client))