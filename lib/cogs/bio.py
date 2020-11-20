from discord.ext.commands import Cog, command, BucketType, cooldown
from discord import Embed, Colour

from ..db import db # pylint: disable=relative-beyond-top-level

from aiohttp import request

from datetime import datetime

from typing import Optional

import os
from dotenv import load_dotenv
load_dotenv()

class Bio(Cog):
    def __init__(self, bot):
        self.bot = bot


    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("bio")

def setup(bot):
	bot.add_cog(Bio(bot))