from discord.ext.commands import Cog, command
from discord import Embed, colour

from ..db import db  # pylint: disable=relative-beyond-top-level

import json

import requests

with open("config.json") as config_file:
    config = json.load(config_file)


class DogeHouse(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="dogehosue", aliases=["dh"], brief="Dogehouse.tv Statistics!")
    async def dogehosue_command(self, ctx):
        response = requests.get(url="https://api.dogehouse.xyz/v1/statistics")
        data = response.json()

        embed = Embed(
            title="DogeHouse Stats!",
            description="https://dogehouse.tv/",
        )

        if response.status_code == 200:
            fields = [
                ("Total Rooms", data["totalRooms"], False),
                ("Total Scheduled Rooms", data["totalScheduledRooms"], False),
                ("Total Online", data["totalOnline"], False),
            ]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            embed.set_footer(text="Timestamp: " + data["timestamp"])

            embed.set_thumbnail(
                url="https://github.com/benawad/dogehouse/blob/staging/feta/assets/regular-doge.png?raw=true"
            )

            await ctx.reply(embed=embed)
        else:
            await ctx.reply(
                f"⚠The DogeHouse API responded with a `{response.status_code}` status code."
            )

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("dogehouse")


def setup(bot):
    bot.add_cog(DogeHouse(bot))
