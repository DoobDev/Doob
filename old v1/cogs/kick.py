import discord
from discord.ext import commands
doob_logo = "https://cdn.discordapp.com/avatars/680606346952966177/ada47c5940b5cf8f7e12f61eefecc610.webp?size=1024"

class kick(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    # Kicks a user that the user provides.
    @commands.command(aliases=['k'])
    # Checks to see if user has the Kick Members permission
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user : discord.Member, *, reason=None):
        await user.kick(reason=reason)
        embed = discord.Embed(title="User Kicked", description=f"{user.name} has been kicked from the server.", colour=discord.Color.blue())

        embed.add_field(name="User", value=f"@{user.name}#{user.discriminator}")
        embed.add_field(name="Reason", value=f"{reason}")
        embed.set_thumbnail(url=doob_logo)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(kick(client))