import discord
from discord.ext import commands

class nitroboost(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Gives user the benefit of Nitro Boosting a server
    @commands.command(hidden=True, aliases=['boost'])
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def nitroboost(self, ctx):
        embed = discord.Embed(title="Nitro Boosting", description="Using your Nitro Boost on a server gives the server...", colour=discord.Color.magenta())

        embed.add_field(name="Pink Role", value="Special Pink Role only given to Nitro Boosters, that can be given special permissions.")
        embed.add_field(name="More Emojis", value="More emojis for the entire server to use. (up to a total of 250 emojis!)")
        embed.add_field(name="Higher Bitrate", value="Higher quality voice channels for the entire server.")
        embed.add_field(name="Special Badge", value="You get a special badge on your Discord profile as well as on the member list.")
        embed.add_field(name="The rest is up to the server.", value="The server can give you secret channels and more perks. For example, mmatt studios gives boosters more role colors, file upload access, file embed access, and more.")
        embed.set_thumbnail(url="https://media1.tenor.com/images/c1ee5ae3e9db6a5a3536f4232e946155/tenor.gif")

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(nitroboost(client))