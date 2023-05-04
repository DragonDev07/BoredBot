import discord
from discord.ext import commands
from discord import app_commands

class Greetings(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Log that the cog has been loaded
    @commands.Cog.listener()
    async def on_ready(self):
        print("The 'Greetings' cog has been loaded")

    # Propagate the error to the global error handler
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await self.bot.on_command_error(ctx, error)

    # "hello" command describing what the bot is and why I made it
    @app_commands.command()
    async def hello(self, interaction: discord.Interaction):
        embed = discord.Embed(title = "Hello!", description = "Hello, I'm Bored, Bored Bot. I was made by Teo when he was bored, have fun!", colour = discord.Colour.blurple())
        await interaction.response.send_message(embed=embed)
        print(f"The 'hello' command was run by {interaction.user}")

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