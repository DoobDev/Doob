import discord
from discord.ext import commands

class profile(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Gives user info to the user
    @commands.command(aliases=['userinfo'])
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def profile(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member


        embed = discord.Embed(title=f"Here is some info I found on {member.name}.", description=f"Info on {member.name}", colour=discord.Color.blue())

        embed.add_field(name="Name", value=member.name)
        embed.add_field(name="Discriminator", value=member.discriminator)
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Current Status", value=member.status)
        embed.add_field(name="Joined this server at:", value=member.joined_at)
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(profile(client))