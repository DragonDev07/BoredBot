import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Log that the cog has been laoded
    @commands.Cog.listener()
    async def on_ready(self):
        print("The 'Help' cog has been loaded")

    @commands.hybrid_command()
    async def help(self, ctx):
        embed = discord.Embed(title = "Help", description = "Bot Help!", colour = discord.Colour.dark_gold())
        embed.add_field(name = "Commands!", value = ">hello - Bot will introduce itself, and describe why it was made\n>kick <member> <optional: reason> - Kicks a given member, requires the user to be able to kick members normally,\n>ban <member> <optional: reason> - Bans provided member, requires user to be able to ban members normally\n>clear <num messages (default 10)> - clears x amount of messages from the channel.", inline = False)
        await ctx.send(embed = embed)
        print(f"The 'help' command was run by {ctx.message.author}")


async def setup(client):
    await client.add_cog(Help(client))