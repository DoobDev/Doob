import discord
from discord.ext import commands

class serverinfo(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    # Gives server info to the user.
    @commands.command(aliases=['server'])
    async def serverinfo(self, ctx):
        await ctx.send("I'm sorry, this command is under construction and is not working\n[Unless the info did send out correctly, please let the dev know,]")
        embed = discord.Embed(title=f"Here is some info i found about {ctx.guild.name}.", description="Server Info.", colour=discord.Color.blue())

        embed.add_field(name="Name", value=ctx.guild.name)
        embed.add_field(name="ID", value=ctx.guild.id)
        embed.add_field(name="Roles", value=ctx.guild.roles)
        embed.add_field(name="Members", value=ctx.guild.members)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(serverinfo(client))