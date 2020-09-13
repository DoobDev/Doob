import discord
from discord.ext import commands
doob_logo = "https://cdn.discordapp.com/avatars/680606346952966177/ada47c5940b5cf8f7e12f61eefecc610.webp?size=1024"

class vote(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["upvote"])
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def vote(self, ctx):
        embed = discord.Embed(title="Vote", description="Vote on Doob bot on...", colour=discord.Color.blue())

        embed.add_field(name="Top.gg", value="https://top.gg/bot/680606346952966177/vote")
        embed.set_thumbnail(url="https://www.flaticon.com/svg/static/icons/svg/2928/2928967.svg")

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(vote(client))
