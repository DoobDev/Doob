import discord
from discord.ext import commands
doob_logo = "https://cdn.discordapp.com/avatars/680606346952966177/ada47c5940b5cf8f7e12f61eefecc610.webp?size=1024"

owner_id = "308000668181069824"

class stream(commands.Cog):
    def __init__(self, client):
        self.client = client
    # Decorator for commands.
    @commands.command()
    @commands.is_owner()
    async def streamstatus(self, ctx, client):
        await client.change_presence(activity=discord.Streaming(name="STREAMING!", url="https://twitch.tv/mmattbtw"))
        await ctx.send("The status has been changed to the Streaming profile!")

    @commands.command()
    @commands.is_owner()
    async def normalstatus(self, ctx, client):
        await client.change_presence(status = discord.Status.online, activity=discord.Game('-help for commands. | github.com/doobdev/doob'))
        await ctx.send("The status has been changed to the Default profile!")

def setup(client):
    client.add_cog(stream(client))