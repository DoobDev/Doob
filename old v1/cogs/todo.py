import discord
from discord.ext import commands
doob_logo = "https://cdn.discordapp.com/avatars/680606346952966177/ada47c5940b5cf8f7e12f61eefecc610.webp?size=1024"

class todo(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    # Gives the todo list from GitHub.
    @commands.command(aliases=['board', 'whatsnext', 'update'])
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def todo(self, ctx):
        embed = discord.Embed(title="Here's the link for what's up next for Doob.", description="The Todo list for Doob.", colour=discord.Color.blue())

        embed.add_field(name="GitHub Issue Board", value="https://github.com/mmatt625/doob/projects/1")
        embed.set_thumbnail(url="https://www.flaticon.com/svg/static/icons/svg/2905/2905140.svg")
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(todo(client))