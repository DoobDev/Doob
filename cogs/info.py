import discord
from discord.ext import commands
doob_logo = "http://i.mmatt.pw/bz0i1U0V"

class info(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Gives user some info about Doob
    @commands.command(aliases=['botinfo'])
    async def info(self, ctx):
        embed = discord.Embed(title="Doob's Info", description="Some of doobs info that might be useful for you to know!", colour=discord.Color.blue())

        embed.add_field(name="Name", value="Doob")
        embed.add_field(name="Description", value="A Discord bot made by mmatt using discord.py, he felt like making it so he did B)")
        embed.add_field(name="Developer", value="The creator of Doob is <@308000668181069824>")
        embed.add_field(name="Hosted on", value="AWS Server")
        embed.add_field(name="Bot's Server Count", value=str(len(client.servers)))
        embed.add_field(name="The ping for Doob is...", value=f" :ping_pong: {round(self.client.latency * 1000)} ms")
        embed.add_field(name="Library", value="discord.py")
        embed.add_field(name="Top.gg Link", value="https://top.gg/bot/680606346952966177")
        embed.add_field(name="Invite Link", value="https://discordapp.com/oauth2/authorize?client_id=680606346952966177&scope=bot&permissions=271674430")
        embed.add_field(name="GitLab Repository", value="https://github.com/mmatt625/doob")
        embed.set_thumbnail(url=doob_logo)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(info(client))
