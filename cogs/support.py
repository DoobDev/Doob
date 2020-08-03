import discord
from discord.ext import commands
doob_logo = "https://cdn.discordapp.com/avatars/680606346952966177/ada47c5940b5cf8f7e12f61eefecc610.webp?size=1024"

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
