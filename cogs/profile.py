import discord
from discord.ext import commands

class profile(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Gives user info to the user
    @commands.command(aliases=['userinfo'])
    async def profile(self, ctx, user: discord.Member):

        embed = discord.Embed(title=f"Here is some info I found on {user.name}.", description=f"Info on {user.name}", colour=discord.Color.blue())

        embed.add_field(name="Name", value=user.name)
        embed.add_field(name="Discriminator", value=user.discriminator)
        embed.add_field(name="ID", value=user.id)
        embed.add_field(name="Current Status", value=user.status)
        embed.add_field(name="Joined this server at:", value=user.joined_at)
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(profile(client))