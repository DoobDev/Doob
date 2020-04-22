import discord
from discord.ext import commands
doob_logo = "http://i.mmatt.pw/bz0i1U0V"

class support(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Gives user the Support Discord + Dev's discord tag if they need help.
    @commands.command()
    async def support(self, ctx):
        embed = discord.Embed(title="Need Support?", description="The Discord Support Server and the dev's contact.", colour=discord.Color.blue(), url="https://discord.gg/ryTYWjD")

        embed.add_field(name="Contact the Dev", value="<@308000668181069824>")
        embed.add_field(name="Join the Discord", value="https://discord.gg/ryTYWjD")
        embed.set_thumbnail(url=doob_logo)

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(support(client))
