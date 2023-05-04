import discord
from discord.ext import commands
from discord import app_commands

class AdminUtils(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Log that the Cog has been loaded
    @commands.Cog.listener()
    async def on_ready(self):
        print("The 'AdminUtils' cog has been loaded")

    # Propagate the error to the global error handler
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await self.bot.on_command_error(ctx, error)

    # Command to kick a member
    @app_commands.command()
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, *, reason: str=None):
        embed = discord.Embed(title="The Kick Hammer", colour=discord.Colour.blurple())
        embed.add_field(name = f"Kicked {member}", value = f"Reason: {reason}")
        await member.kick(reason=reason)
        await interaction.response.send_message(embed=embed)
        print(f"The 'kick' command has been run on {member} by {interaction.user} for reason {reason}")
    
    # Command to ban a member
    @app_commands.command()
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, *, reason: str=None):
        embed = discord.Embed(title="The Ban Hammer", colour=discord.Colour.blurple())
        embed.add_field(name = f"Banned {member}", value = f"Reason: {reason}")
        await member.ban(reason=reason)
        await interaction.response.send_message(embed=embed)
        print(f"The 'ban' command has been run on {member} by {interaction.user} for reason {reason}")

    # Command to clear x amount of messages in a channel
    @app_commands.command()
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, amount: int = 10):
        embed = discord.Embed(title = "Cleared Messages!", colour = discord.Colour.blurple())
        embed.add_field(name="", value = f"Cleared {amount} previous messages")
        await interaction.response.send_message(f"Clearing the last {amount} messages")
        await interaction.channel.purge(limit=amount)
        await interaction.channel.send(embed=embed)
        print(f"The 'clear' command was run by {interaction.user} for amount {amount}")

    # Command to get the info of a given user
    # @app_commands.command()
    # @app_commands.checks.has_permissions(manage_nicknames=True)
    # async def info(self, interaction: discord.Interaction, user: discord.User):
    #     embed = discord.Embed(title ="Userinfo", description = f"The info of {user.name}", color = discord.Colour.blue())
    #     embed.add_field(name = user, value = f"-User\'s name: {user.name}\n -User\'s ID {user.id}\n -User\'s discrim: {user.discriminator}\n -User\'s Avatar Hash: {user.avatar}")
    #     await interaction.response.send_message(embed = embed)
    #     print(f"The 'userinfo' command was just run by {interaction.user} to get info on {user}")

    @app_commands.command()
    @app_commands.checks.has_permissions(manage_nicknames=True)
    async def getinfo(self, interaction: discord.Interaction, user: discord.User):
        embed = discord.Embed(title = f"{user.name}'s Info", colour = discord.Colour.blurple())
        embed.add_field(name = "User's Name:", value = f"{user.name}")
        embed.add_field(name = "User's ID:", value = f"{user.id}")
        embed.add_field(name = "User's Discrim:", value = f"{user.discriminator}")
        embed.add_field(name = "User's Avatar Hash:", value = f"{user.avatar}")

        await interaction.response.send_message(embed=embed)
        print(f"The 'userinfo' command was just run by {interaction.user} to get info on {user}")
    
async def setup(client):
    await client.add_cog(AdminUtils(client))