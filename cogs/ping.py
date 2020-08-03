import discord
from discord.ext import commands
doob_logo = "https://cdn.discordapp.com/avatars/680606346952966177/ada47c5940b5cf8f7e12f61eefecc610.webp?size=1024"

class ping(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Ping command, gives latency of the bot to the user.
    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed(title="Pong!", description=":ping_pong:", colour=discord.Color.blue())

        embed.add_field(name="The latency for Doob is...", value=f"{round(self.client.latency * 1000)} ms")
        embed.set_thumbnail(url=doob_logo)

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(ping(client))