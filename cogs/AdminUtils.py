import discord
from discord.ext import commands

class AdminUtils(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Log that the Cog has been loaded
    @commands.Cog.listener()
    async def on_ready(self):
        print("The 'AdminUtils' cog has been loaded")

    # Command to kick a member
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"Kicked User {member} for reason {reason}")
        print(f"The 'kick' command has been run on {member} by {ctx.message.author} for reason {reason}")
    
    # Command to ban a member
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"User {member} has been yeeted (banned) for reason {reason}")
        print(f"The 'ban' command has been run on {member} by {ctx.message.author} for reason {reason}")
    
    # Command to clear x amount of messages in a channel
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=10):
        await ctx.channel.purge(limit=amount)
        await ctx.send(f"Cleared the last {amount} messages")
        print(f"The 'clear' command was run by {ctx.message.author}")

    # Command to Sync slash commands and be recognized by discord
    @commands.command()
    async def sync_commands(self, ctx):
        await self.client.tree.sync()
        await ctx.send("Commands synced!")
        print(f"The 'sync_commands' command was run by {ctx.message.author}")
    
async def setup(client):
    await client.add_cog(AdminUtils(client))