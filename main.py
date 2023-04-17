import discord
import os
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='>', intents=intents)

@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game("I was bored, now this bot exists. Use '>help' for commands.")
    )
    print("Bot is online, good luck >:)")

@client.command()
async def ping(ctx, user: discord.User, *, message=None):
    await ctx.send(f"{user.mention} Pong")
    print("Woah someone ran the ping command on: " + str(user))

client.run('token here pls')
