import discord
from discord.ext import commands
doob_logo = "http://i.mmatt.pw/bz0i1U0V"

class help(commands.Cog):
    def __init__(self, client):
        self.client = client
    # Decorator for commands.
    @commands.command(aliases=['helpme'])
    async def help(self, ctx):
        embed = discord.Embed(title="Command Help", description="All of Doob's commands.", colour=discord.Color.blue())

        embed.add_field(name="Check out the docs!", value="https://notmmatt.gitbook.io/docs/")
        embed.add_field(name="Join the Support Discord", value="https://discord.gg/ryTYWjD")
        embed.set_thumbnail(url=doob_logo)

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(help(client))
