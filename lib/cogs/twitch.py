from discord.ext.commands import Cog, command, BucketType, cooldown

from ..db import db # pylint: disable=relative-beyond-top-level

from aiohttp import request

from typing import Optional

import os
from dotenv import load_dotenv
load_dotenv()

class Twitch(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="streamlookup", aliases=["lookup", "twitch", "twitchsearch", "twitchlookup"], brief="Get Twitch stream information.")
    @cooldown(1, 5, BucketType.user)
    async def stream_lookup_command(self, ctx, *, username: Optional[str]):
        """Request some information on a specific Twitch Stream!"""

        User_URL = f"https://api.twitch.tv/helix/users?login={username}"

        async with request("GET", User_URL, headers={[Client-ID=os.environ.get("twitchclientid")}]) as response:
            response.status == 200:
                data = await response.json()

        User_ID = data["data", "id"]

        print(User_ID)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("twitch")

def setup(bot):
	bot.add_cog(Twitch(bot))