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
    print("-------------------------------")

initial_extensions = []

for filename in os.istdir('./cogs'):
    if filename.endswith('.py'):
        initial_extensions.append("cogs." + filename[:-3])


client.run(TOKEN)