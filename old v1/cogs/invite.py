import discord
from discord.ext import commands
doob_logo = "https://cdn.discordapp.com/avatars/680606346952966177/ada47c5940b5cf8f7e12f61eefecc610.webp?size=1024"

class invite(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    # Gives user the invite link to Doob.
    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def invite(self, ctx):
        embed = discord.Embed(title="Invite", description="Invite Doob to your server!", colour=discord.Color.blue(), url="https://discordapp.com/oauth2/authorize?client_id=680606346952966177&scope=bot&permissions=271674430")

        embed.add_field(name="Click here to invite Doob to your Discord Server.", value="https://discordapp.com/oauth2/authorize?client_id=680606346952966177&scope=bot&permissions=271674430")
        embed.set_thumbnail(url=doob_logo)

        await ctx.send(embed=embed)


    
def setup(client):
    client.add_cog(invite(client))
