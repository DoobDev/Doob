from discord.ext.commands import Cog, command, BucketType, cooldown
from discord import Embed, Colour

from ..db import db # pylint: disable=relative-beyond-top-level

from aiohttp import request

from datetime import datetime

from typing import Optional

import os
from dotenv import load_dotenv
load_dotenv()

class Twitch(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="streamlookup", aliases=["lookup", "twitch", "twitchsearch", "twitchlookup"], brief="Get Twitch stream information.")
    @cooldown(1, 5, BucketType.user)
    async def stream_lookup_command(self, ctx, *, username: str):
        """Request some information on a specific Twitch Stream/User!\n`Username` = Twitch Username"""

        User_URL = f"https://api.twitch.tv/kraken/users?login={username}"
        async with request("GET", User_URL, headers={'Client-ID': os.environ.get("twitchclientid"), 'Accept': 'application/vnd.twitchtv.v5+json'}) as response:
            if response.status == 200:
                User_ID = (await response.json())['users'][0]['_id']

                StreamInfo_URL = f'https://api.twitch.tv/kraken/streams/{User_ID}'

                async with request("GET", StreamInfo_URL, headers={'Client-ID': os.environ.get("twitchclientid"), 'Accept': 'application/vnd.twitchtv.v5+json'}) as response2:
                    if response2.status == 200:
                        if (await response2.json())['stream'] != None:
                            embed = Embed(title=f"{(await response2.json())['stream']['channel']['display_name']} Stream Info", colour=Colour.dark_purple(),  timestamp=datetime.utcnow())

                            fields = [("Name", f"{(await response2.json())['stream']['channel']['display_name']}", False),
                                    ("Title", f"{(await response2.json())['stream']['channel']['status']}", True),
                                    ("Game", f"{(await response2.json())['stream']['channel']['game']}", True),
                                    ("Viewers", f"{(await response2.json())['stream']['viewers']}", True),
                                    ("Lagnuage", f"{(await response2.json())['stream']['channel']['broadcaster_language']}", True),
                                    ("Followers", f"{(await response2.json())['stream']['channel']['followers']}", True),
                                    ("Patner Status", f"{(await response2.json())['stream']['channel']['partner']}", True),
                                    ("Went live at:", f"{(await response2.json())['stream']['created_at']}", True),]

                            for name, value, inline in fields:
                                embed.add_field(name=name, value=value, inline=inline)

                            embed.set_image(url=(await response2.json())['stream']['preview']['large'])
                            embed.set_thumbnail(url=(await response2.json())['stream']['channel']['logo'])

                            await ctx.send(embed=embed)

                        else:
                            UserInfo_URL = f'https://api.twitch.tv/kraken/users/{User_ID}'
                            async with request("GET", UserInfo_URL, headers={'Client-ID': os.environ.get("twitchclientid"), 'Accept': 'application/vnd.twitchtv.v5+json'}) as response3:
                                embed = Embed(title=f"{(await response3.json())['display_name']} User Info", colour=ctx.author.colour, timestamp=datetime.utcnow())

                                fields = [("Name", (await response3.json())["display_name"], False),
                                            ("Bio", (await response3.json())["bio"], False),
                                            ("Account Type", (await response3.json())["type"], False),
                                            ("Creation Date", (await response3.json())["created_at"], False),
                                            ("Last Updated", (await response3.json())["updated_at"], False)]

                                for name, value, inline in fields:
                                    embed.add_field(name=name, value=value, inline=inline)

                                embed.set_thumbnail(url=(await response3.json())["logo"])

                                await ctx.send(embed=embed)
                            

    @stream_lookup_command.error
    async def stream_lookup_command_error(self, ctx, exc):
        if hasattr(exc, "original"):
            if isinstance(exc.original, IndexError):
                await ctx.send("User does not seem to exist on Twitch.tv")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("twitch")

def setup(bot):
	bot.add_cog(Twitch(bot))