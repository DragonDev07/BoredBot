import discord
from discord.ext import commands

class DevCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.blocked_users = set()

    

    # Log that the cog was loaded
    @commands.Cog.listener()
    async def on_ready(self):
        print("The 'DevCommands' cog has been loaded")

    # Propagate the error to the global error handler
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await self.bot.on_command_error(ctx, error)

    # Command to load given cog
    @commands.command()
    @commands.is_owner()
    async def loadcog(self, ctx, cogname=None):
        if cogname is None:
            await ctx.send("Please provide a cog to load.")
            return
        try:
            cog = "cogs." + cogname
            await self.client.load_extension(cog)
        except Exception as e:
            await ctx.send(f"Loading cog {cogname} threw error {e}. Did not load cog.")
        else:
            await ctx.send("Loaded Cog!")
        print(f"The 'loadcog' command was run by {ctx.message.author}")

    # Command that unloads the given cog 
    @commands.command()
    @commands.is_owner()
    async def unloadcog(self, ctx, cogname=None):
        if cogname is None:
            await ctx.send("Please provide a cog to unload.")
            return
        try:
            cog = "cogs." + cogname
            await self.client.unload_extension(cog)
        except Exception as e:
           await ctx.send(f"Unloading cog {cogname} threw error {e}. Did not unload cog.")
        else:
            await ctx.send("Unloaded Cog!")
        print(f"The 'unloadcog' command was run by {ctx.message.author}")

    # Command to Sync slash commands and be recognized by discord
    @commands.command()
    @commands.is_owner()
    async def sync_commands(self, ctx):
        await self.client.tree.sync()
        await ctx.send("Commands synced!")
        print(f"The 'sync_commands' command was run by {ctx.message.author}")

    # Command to spectator mode, deletes messages and reactions when sent
    @commands.command()
    @commands.is_owner()
    async def mute(self, ctx, user: discord.User):
        self.blocked_users.add(user.id)
        await ctx.send(f'{user.name} has been muted.')
    
    @commands.command()
    @commands.is_owner()
    async def unmute(self, ctx, user: discord.User):
        self.blocked_users.remove(user.id)
        await ctx.send(f"{user.name} has been unmuted")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        if message.author.id in self.blocked_users:
            await message.delete()
        await self.client.process_commands(message)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.id in self.blocked_users:
            await reaction.remove(user)
        
async def setup(client):
    await client.add_cog(DevCommands(client))