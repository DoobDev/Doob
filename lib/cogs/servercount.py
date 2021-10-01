"""
UPDATES Doob's SERVER COUNT ON TOPGG
"""
import logging
import dbl

from discord.ext import commands

import os
from dotenv import load_dotenv

load_dotenv()
log = logging.getLogger()


class ServerCount(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, bot):
        self.bot = bot

        self.dblpy = dbl.DBLClient(
            self.bot, os.environ.get("topgg"), autopost=True
        )  # Autopost will post your guild count every 30 minutes
        log.info("\nTop.gg updated\n")

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("servercount")


def setup(bot):
    bot.add_cog(ServerCount(bot))
