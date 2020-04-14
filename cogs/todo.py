import discord
from discord.ext import commands
doob_logo = "http://i.mmatt.pw/bz0i1U0V"

class todo(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    # Gives the todo list from GitLab.
    @commands.command(aliases=['board', 'whatsnext', 'update'])
    async def todo(self, ctx):
        embed = discord.Embed(title="Here's the link for what's up next for Doob.", description="The Todo list for Doob.", colour=discord.Color.blue())

        embed.add_field(name="GitLab Issue Board", value="https://gitlab.com/mmatt625/doob/-/boards")
        embed.set_thumbnail(url=doob_logo)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(todo(client))