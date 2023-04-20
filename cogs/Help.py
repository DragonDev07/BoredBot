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
        embed = discord.Embed(title = "Help", colour = discord.Colour.dark_gold())
        embed.add_field(name = "Hello!", value = ">hello - Bot will introduce itself, and describe why it was made", inline = False)
        embed.add_field(name = "Prefixes", value = "All comands will work no matter what when prefixed with '>', if you would like to use '/' commands, only some work (no admin util commands work).", inline = False)
        embed.add_field(name = "Media", value = "To Control Media, Use the following commands. Queuing videos is not a feature yet, one videos at a time please.\n• >join - Makes the bot join the vc that you are currently in.\n• >leave - Makes the bot leave the vc it is in.\n• >play <youtube url> - Plays audio from a youtube video\n• >pause - Pauses currently playing audio.\n• >resume - Resumes pasued audio.\n• >stop - Stops Music (not saving current place)\n• >volume <optional: volume (out of 100)> - If provided with a value, will set the volume to that, if value is not provided, will print out current volume.", inline = False)
        embed.add_field(name = "Admin Util Commands", value = "• >kick <member> <optional: reason> - Kicks a given member, requires the user to be able to kick members normally,\n• >ban <member> <optional: reason> - Bans provided member, requires user to be able to ban members normally\n• >clear <num messages (default 10)> - clears x amount of messages from the channel.\n• >userinfo <member> - Provides important details that are mainly used for debug about given user, requires admin.", inline = False)
        embed.add_field(name = "Cogs (DEBUG INFO FOR DEVELOPERS)", value = "• Greetings\n• AdminUtils\n• Help\n• Media\n• DevCommands", inline = False)
        embed.add_field(name = "Created w/ ❤️ by:", value = "Teo Welton (FurthestDrop517#9625). Enjoy!\n (if you wanna contribute run >contributing)", inline = False)
        await ctx.send(embed = embed)
        print(f"The 'help' command was run by {ctx.message.author}")

    @commands.hybrid_command()
    async def contributing(self, ctx):
        embed = discord.Embed(title = "Contribute (For Developers!)", description = "Developers! Do you want to contribute? Come on over to github!", colour = discord.Colour.yellow())
        embed.add_field(name = "Github Repository", value = "Checkout the repo and contribute at https://github.com/DragonDev07/im-bored-discord-bot", inline = False)
        await ctx.send(embed = embed)

async def setup(client):
    await client.add_cog(Help(client))