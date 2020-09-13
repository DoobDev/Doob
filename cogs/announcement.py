import discord
from discord.ext import commands
doob_logo = "https://cdn.discordapp.com/avatars/680606346952966177/ada47c5940b5cf8f7e12f61eefecc610.webp?size=1024"

class announcement(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def announcement(self, ctx):
        embed = discord.Embed(title = "Announcement:", description = f"{ctx.message.content.replace(f'{command_prefix}announcement ', '')}")
        embed.set_footer(text=f"Announcement from: {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
        await ctx.channel.purge(limit=1)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(announcement(client))
