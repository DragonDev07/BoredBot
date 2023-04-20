import asyncio
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# TOKEN = os.environ.get('DISCORD_BOT_TOKEN') # Actual Bot Token
TOKEN = os.environ.get('TESTING_BOT_TOKEN') # Testing Bot Token

intents = discord.Intents.all()
intents.message_content = True
client = commands.Bot(command_prefix='>', intents=intents, help_command=None)

@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game("I was bored, now this bot exists. Use '>help' for commands."))
    print("Bot is online, good luck >:)")
    print("-------------------------------")

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f'cogs.{filename[:-3]}')

async def main():
    await load()
    await client.start(TOKEN)

asyncio.run(main())