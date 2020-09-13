import discord
from discord.ext import commands
doob_logo = "https://cdn.discordapp.com/avatars/680606346952966177/ada47c5940b5cf8f7e12f61eefecc610.webp?size=1024"

class errors(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Error handling.
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Missing Requirement Error [DB10]", description="Pass in all required arguments.", colour=discord.Color.red())
            embed.set_thumbnail(url="https://www.flaticon.com/svg/static/icons/svg/745/745419.svg")
            await ctx.send(embed=embed, delete_after = 15)
        else:
            raise error

        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title="Missing Permissions Error [DB11]", description="You are not able to use this command because you do not have the required permissions.", colour=discord.Color.red())
            embed.set_thumbnail(url="https://www.flaticon.com/svg/static/icons/svg/745/745419.svg")
            await ctx.send(embed=embed, delete_after = 15)
        else:
            raise error

        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title="Cooldown", description="You are on cooldown! Please try again in {:.2f}s".format(error.retry_after), colour=discord.Color.red())
            embed.set_thumbnail(url="https://www.flaticon.com/svg/static/icons/svg/1620/1620451.svg")
            await ctx.send(embed=embed, delete_after = error.retry_after)
        else:
            raise error
        
        if isinstance(error, commands.ArgumentParsingError):
            embed = discord.Embed(title="Argument Parsing Error [DB12]", description="An exception raised when the parser fails to parse a user’s input.", colour=discord.Color.red())
            embed.set_thumbnail(url="https://www.flaticon.com/svg/static/icons/svg/745/745419.svg")
            await ctx.send(embed=embed, delete_after= 15)
        else:
            raise error

        if isinstance(error, commands.PrivateMessageOnly):
            embed = discord.Embed(title="Private Message Only [DB13]", description="This command does not work in a server, only in ")
            embed.set_thumbnail(url="https://www.flaticon.com/svg/static/icons/svg/745/745419.svg")
            await ctx.send(embed=embed, delete_after= 15)
        else:
            raise error
        if isinstance(error, commands.NoPrivateMessage):
            embed=discord.Embed(title="No Private Message [DB14]", description="This command doesn't work in PMs")
            embed.set_thumbnail(url="https://www.flaticon.com/svg/static/icons/svg/745/745419.svg")
            await ctx.send(embed=embed, delete_after= 15)
        else:
            raise error

        if isinstance(error, commands.DisabledCommand):
            embed = discord.Embed(title="Command Disabled [DB15]", description="This command has been disabled.")
            embed.set_thumbnail(url="https://www.flaticon.com/svg/static/icons/svg/745/745419.svg")
            await ctx.send(embed=embed, delete_after= 15)
        else:
            raise error

        if isinstance(error, commands.NotOwner):
            embed = discord.Embed(title="Not Owner [DB16]", description="This is a owner only command.")
            embed.set_thumbnail(url="https://www.flaticon.com/svg/static/icons/svg/745/745419.svg")
            await ctx.send(embed=embed, delete_after= 15)
        else:
            raise error

        if isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(title="Bot Missing Permissions [DB17]", description="Doob is missing permissions, that are needed to execute this command.")
            embed.set_thumbnail(url="https://www.flaticon.com/svg/static/icons/svg/745/745419.svg")
            await ctx.send(embed=embed, delete_after= 15)
        else:
            raise error

def setup(client):
    client.add_cog(errors(client))