import discord
from discord.ext import commands
doob_logo = "https://cdn.discordapp.com/avatars/680606346952966177/ada47c5940b5cf8f7e12f61eefecc610.webp?size=1024"

class help(commands.Cog):
    def __init__(self, client):
        self.client = client
    # Decorator for commands.
    @commands.command(aliases=['helpme'])
    async def help(self, ctx):
        embed = discord.Embed(title="Command Help", description="All of Doob's commands.", colour=discord.Color.blue())

        embed.add_field(name="Check out the docs!", value="http://docs.doobbot.com/")
        embed.add_field(name="Join the Support Discord", value="https://discord.gg/ryTYWjD")
        embed.set_thumbnail(url=doob_logo)

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(help(client))
