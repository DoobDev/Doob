import dbl

from discord.ext import commands

import os
from dotenv import load_dotenv

load_dotenv()


class servercount(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, bot):
        self.bot = bot

        self.dblpy = dbl.DBLClient(
            self.bot, os.environ.get("topgg"), autopost=True
        )  # Autopost will post your guild count every 30 minutes
        print("\nTop.gg updated")

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("servercount")


def setup(bot):
    bot.add_cog(servercount(bot))
