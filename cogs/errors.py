import discord
from discord.ext import commands
doob_logo = "http://i.mmatt.pw/bz0i1U0V"

class errors(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Error handling.
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Missing Requirement Error [DB10]", description="Pass in all required arguments.", colour=discord.Color.blue())

            embed.add_field(name="Docs", value="Check out the Docs for more info. - https://www.notion.so/Errors-2516c9ab19a4482c9cc69d4b26c30c4a")

            embed.set_thumbnail(url=doob_logo)
            await ctx.send(embed=embed)

        
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title="Missing Permissions Error [DB11]", description="You are not able to use this command because you do not have the required permissions.", colour=discord.Color.blue())

            embed.add_field(name="Docs", value="Check out the Docs for more info. - https://www.notion.so/Errors-2516c9ab19a4482c9cc69d4b26c30c4a")

            embed.set_thumbnail(url=doob_logo)
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(errors(client))