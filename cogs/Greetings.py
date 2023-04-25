import discord
from discord.ext import commands

class Greetings(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Log that the cog has been loaded
    @commands.Cog.listener()
    async def on_ready(self):
        print("The 'Greetings' cog has been loaded")

    # "hello" command describing what the bot is and why I made it
    @commands.hybrid_command()
    async def hello(self, ctx):
        await ctx.send("Hello, I'm Bored, Bored Bot. I was made by Teo when he was bored, have fun!")
        print(f"The 'hello' command was run by {ctx.message.author}")

    # Send a "Welcome" message when a user joins the server
    @commands.Cog.listener()
    async def on_memeber_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Welcome {member.mention} have f...u...u...u...u...u...n!')
        else:
            print("Could not run on_member_join, channel returned none")

async def setup(client):
    await client.add_cog(Greetings(client))