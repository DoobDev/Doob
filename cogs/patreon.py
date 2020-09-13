import discord
from discord.ext import commands
doob_logo = "https://cdn.discordapp.com/avatars/680606346952966177/ada47c5940b5cf8f7e12f61eefecc610.webp?size=1024"

class patreon(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Patreon Command
    @commands.command(aliases=['donate'])
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def patreon(self, ctx):
        embed = discord.Embed(title="The developer's Patreon is avaliable at:", description="https://patreon.com/doobdev")
        embed.set_thumbnail(url="https://cdn.vox-cdn.com/thumbor/a3z1idZDuso6ksgW6pDOZwCRJDw=/1400x1400/filters:format(jpeg)/cdn.vox-cdn.com/uploads/chorus_asset/file/9833961/patreon.jpg")
        embed.set_footer(text="mmatt thanks you! (doob luvs yuh)", icon_url=doob_logo)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(patreon(client))