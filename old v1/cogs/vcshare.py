import discord
from discord.ext import commands
doob_logo = "https://cdn.discordapp.com/avatars/680606346952966177/ada47c5940b5cf8f7e12f61eefecc610.webp?size=1024"

class vcshare(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Gives user the link to screenshare on Discord without using Go Live.
    @commands.command(aliases=['vc', 'screenshare', 'ss'])
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def vcshare(self, ctx):
        embed = discord.Embed(title="Screenshare", description="Cilck this link to screenshare", colour=discord.Color.blue(), url=f"https://discordapp.com/channels/{ctx.guild.id}/{ctx.author.voice.channel.id}")

        embed.add_field(name="Screenshare here", value=f"https://discordapp.com/channels/{ctx.guild.id}/{ctx.author.voice.channel.id}")
        embed.set_thumbnail(url="https://www.flaticon.com/svg/static/icons/svg/638/638867.svg")

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(vcshare(client))