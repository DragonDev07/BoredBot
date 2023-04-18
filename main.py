import discord
import os
from discord.ext import commands
from discord import FFmpegPCMAudio
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='>', intents=intents)

@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game("I was bored, now this bot exists. Use '>help' for commands."))
    print("Bot is online, good luck >:)")

@client.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
        await ctx.send("Joined VC, playing music!")
    else:
        await ctx.send("You must be in a voice channel to run this command!")
    print("Join Command has been run")

@client.command(pass_context = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Left VC")
    else:
        await ctx.send("I am not in a VC at the moment. Use >join to add me to one!")

@client.command(pass_context = True)
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if (voice.is_playing()):
        voice.pause()
    else:
        await ctx.send("I am not playing anything at the moment")

@client.command(pass_context = True)
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if (voice.is_paused()):
        voice.resume()
    else:
        await ctx.send("No song is paused at the moment!")
    
@client.command()
async def play(ctx, args):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if (args == "song1"):
        source = FFmpegPCMAudio("static_music.mp3")
        await ctx.send("Playing music")
    elif (args == "song2"):
        source = FFmpegPCMAudio("static_music.mp3")
        await ctx.send("Playing other definitly more different music")
    player = voice.play(source)

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.member, *, reason=None):
    await member.kick(reason=reason)
    # await ctx.send("Member " + str(member) + " has been kicked for reason: " + str(reason))

client.run(TOKEN)