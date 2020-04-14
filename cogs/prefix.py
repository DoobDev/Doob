import discord
import json
from discord.ext import commands

doob_logo = "http://i.mmatt.pw/bz0i1U0V"

owner_id = "308000668181069824"

class prefix(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Opens json file then dumps '-'
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(guild.id)] = "-"

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

    # Removes guild from json file when Doob leaves.
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes.pop(str(guild.id))

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

    # Changes the prefix (that the user provides.) for the specific server.
    @commands.command(aliases=['prefix'])
    @commands.has_permissions(administrator=True)
    async def changeprefix(self, ctx, prefix):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        embed = discord.Embed(title="An administrator has changed the prefix.", description=f"The administrator has changed the prfix to {prefix}.", colour=discord.Color.blue())

        embed.add_field(name="The prefix has been changed to:", value=prefix)
        embed.set_thumbnail(url=doob_logo)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def ownerprefixchange(self, ctx, prefix):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        embed = discord.Embed(title="An administrator has changed the prefix.", description=f"The administrator has changed the prfix to {prefix}.", colour=discord.Color.blue())

        embed.add_field(name="The prefix has been changed to:", value=prefix)
        embed.set_thumbnail(url=doob_logo)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(prefix(client))