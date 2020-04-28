import discord
from discord.ext import commands
doob_logo = "http://i.mmatt.pw/bz0i1U0V"

class vote(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["upvote"])
    async def vote(self, ctx):
        embed = discord.Embed(title="Vote", description="Vote on Doob bot on...", colour=discord.Color.blue())

        embed.add_field(name="Top.gg", value="https://top.gg/bot/680606346952966177/vote")
        embed.set_thumbnail(url=doob_logo)

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(vote(client))
