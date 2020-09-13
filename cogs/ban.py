import discord
from discord.ext import commands
doob_logo = "https://cdn.discordapp.com/avatars/680606346952966177/ada47c5940b5cf8f7e12f61eefecc610.webp?size=1024"

class ban(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['b'])
   # Checks to see if user has the Ban Members permission
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user : discord.Member, *, reason=None):
        await user.ban(reason=reason)
        embed = discord.Embed(title="User Banned", description=f"{user.name} has been banned from the server.", colour=discord.Color.blue())

        embed.add_field(name="User", value=f"@{user.name}#{user.discriminator}")
        embed.add_field(name="Reason", value=f"{reason}")
        embed.set_thumbnail(url="https://www.flaticon.com/svg/static/icons/svg/492/492570.svg")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(ban(client))