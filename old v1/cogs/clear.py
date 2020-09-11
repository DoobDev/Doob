import discord
from discord.ext import commands
doob_logo = "https://cdn.discordapp.com/avatars/680606346952966177/ada47c5940b5cf8f7e12f61eefecc610.webp?size=1024"

class clear(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Clears amount of messages the user provided.
    @commands.command(aliases=['p', 'c', 'purge'])
    # Checks to see if user has the Manage Messages permission
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5):
        embed = discord.Embed(title="Cleared Messages", description="Purge has been executed.", colour=discord.Color.blue())

        embed.add_field(name="Cleared", value=f"{amount} messages")

        await ctx.channel.purge(limit=amount + 1)
        embed.set_thumbnail(url=doob_logo)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(clear(client))