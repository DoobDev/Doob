"""
NEVER GOING TO BE IN USE.
FROM TESTING SLASH COMMANDS
"""

from discord.ext.commands import Cog, command, cooldown, BucketType

import discord

from ..db import db  # pylint: disable=relative-beyond-top-level

import json

from discord_slash import cog_ext, SlashContext


with open("config.json") as config_file:
    config = json.load(config_file)

guild_ids = [702352937980133386]


class Slash(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("slash")

    @cog_ext.cog_slash(name="test", guild_ids=guild_ids)
    async def _test(self, ctx: SlashContext):
        embed = discord.Embed(title="embed test")
        await ctx.send(content="test", embeds=[embed])


def setup(bot):
    bot.add_cog(Slash(bot))
