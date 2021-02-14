from discord.ext.commands import Cog, command, BucketType, cooldown, group
from discord import Embed, Colour

from ..db import db  # pylint: disable=relative-beyond-top-level

from aiohttp import request

from datetime import datetime

from typing import Optional

import os
from dotenv import load_dotenv

load_dotenv()


class Twitch(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def twitch_search(self, ctx, username: str):
        User_URL = f"https://api.twitch.tv/kraken/users?login={username}"
        async with request(
            "GET",
            User_URL,
            headers={
                "Client-ID": os.environ.get("twitchclientid"),
                "Accept": "application/vnd.twitchtv.v5+json",
            },
        ) as response:
            if response.status == 200:
                User_ID = (await response.json())["users"][0]["_id"]

                StreamInfo_URL = f"https://api.twitch.tv/kraken/streams/{User_ID}"

                async with request(
                    "GET",
                    StreamInfo_URL,
                    headers={
                        "Client-ID": os.environ.get("twitchclientid"),
                        "Accept": "application/vnd.twitchtv.v5+json",
                    },
                ) as response2:
                    if response2.status == 200:
                        if (await response2.json())["stream"] != None:
                            embed = Embed(
                                title=f"{(await response2.json())['stream']['channel']['display_name']} Stream Info",
                                colour=Colour.dark_purple(),
                                timestamp=datetime.utcnow(),
                            )

                            fields = [
                                (
                                    "Name",
                                    f"{(await response2.json())['stream']['channel']['display_name']}",
                                    False,
                                ),
                                (
                                    "Title",
                                    f"{(await response2.json())['stream']['channel']['status']}",
                                    True,
                                ),
                                (
                                    "Game",
                                    f"{(await response2.json())['stream']['channel']['game']}",
                                    True,
                                ),
                                (
                                    "Viewers",
                                    f"{(await response2.json())['stream']['viewers']}",
                                    True,
                                ),
                                (
                                    "Lagnuage",
                                    f"{(await response2.json())['stream']['channel']['broadcaster_language']}",
                                    True,
                                ),
                                (
                                    "Followers",
                                    f"{(await response2.json())['stream']['channel']['followers']}",
                                    True,
                                ),
                                (
                                    "Patner Status",
                                    f"{(await response2.json())['stream']['channel']['partner']}",
                                    True,
                                ),
                                (
                                    "Went live at:",
                                    f"{(await response2.json())['stream']['created_at']}",
                                    True,
                                ),
                                (
                                    "URL",
                                    (await response2.json())["stream"]["channel"][
                                        "url"
                                    ],
                                    False,
                                ),
                            ]

                            for name, value, inline in fields:
                                embed.add_field(name=name, value=value, inline=inline)

                            embed.set_image(
                                url=(await response2.json())["stream"]["preview"][
                                    "large"
                                ]
                            )
                            embed.set_thumbnail(
                                url=(await response2.json())["stream"]["channel"][
                                    "logo"
                                ]
                            )

                            await ctx.reply(embed=embed)

                        else:
                            UserInfo_URL = (
                                f"https://api.twitch.tv/kraken/channels/{User_ID}"
                            )
                            UserInfo2_URL = (
                                f"https://api.twitch.tv/kraken/users/{User_ID}"
                            )
                            async with request(
                                "GET",
                                UserInfo_URL,
                                headers={
                                    "Client-ID": os.environ.get("twitchclientid"),
                                    "Accept": "application/vnd.twitchtv.v5+json",
                                },
                            ) as response3:
                                async with request(
                                    "GET",
                                    UserInfo2_URL,
                                    headers={
                                        "Client-ID": os.environ.get("twitchclientid"),
                                        "Accept": "application/vnd.twitchtv.v5+json",
                                    },
                                ) as response4:
                                    embed = Embed(
                                        title=f"{(await response3.json())['display_name']} User Info",
                                        colour=ctx.author.colour,
                                        timestamp=datetime.utcnow(),
                                    )

                                    fields = [
                                        (
                                            "Name",
                                            (await response3.json())["display_name"],
                                            False,
                                        ),
                                        ("Bio", (await response4.json())["bio"], False),
                                        (
                                            "Account Type",
                                            (await response4.json())["type"],
                                            True,
                                        ),
                                        (
                                            "Creation Date",
                                            (await response3.json())["created_at"],
                                            False,
                                        ),
                                        (
                                            "Last Updated",
                                            (await response3.json())["updated_at"],
                                            False,
                                        ),
                                        (
                                            "Followers",
                                            (await response3.json())["followers"],
                                            True,
                                        ),
                                        (
                                            "Partner Status",
                                            (await response3.json())["partner"],
                                            True,
                                        ),
                                        (
                                            "Language",
                                            (await response3.json())["language"],
                                            True,
                                        ),
                                        ("URL", (await response3.json())["url"], False),
                                    ]

                                    for name, value, inline in fields:
                                        embed.add_field(
                                            name=name, value=value, inline=inline
                                        )

                                    embed.set_thumbnail(
                                        url=(await response3.json())["logo"]
                                    )

                                    if (await response3.json())[
                                        "profile_banner"
                                    ] != None:
                                        embed.set_image(
                                            url=(await response3.json())[
                                                "profile_banner"
                                            ]
                                        )

                                    await ctx.reply(embed=embed)

    @group(
        name="twitch",
        aliases=["lookup", "streamlookup", "twitchsearch", "twitchlookup", "stream"],
        brief="Get Twitch stream information.",
    )
    @cooldown(1, 5, BucketType.user)
    async def twitch(self, ctx):
        """Request some information on a specific Twitch Stream/User!\n`Username` = Twitch Username"""
        if ctx.invoked_subcommand is None:
            await ctx.reply("Doing `d!twitch` doesn't work anymore! Looking to search someone? Try `d!twitch -search {username}`")

    @twitch.command(name="-search", aliases=["-s"])
    async def twitch_search_command(self, ctx, username: str):
        await self.twitch_search(ctx, username=username)

    @twitch_search_command.error
    async def twitch_search_command_error(self, ctx, exc):
        if hasattr(exc, "original"):
            if isinstance(exc.original, IndexError):
                await ctx.reply("User does not seem to exist on Twitch.tv")

    @twitch.command(name="-title", aliases=["-t"])
    async def twitch_title_command(self, ctx, username: str):
        User_URL = f"https://api.twitch.tv/kraken/users?login={username}"
        async with request(
            "GET",
            User_URL,
            headers={
                "Client-ID": os.environ.get("twitchclientid"),
                "Accept": "application/vnd.twitchtv.v5+json",
            },
        ) as response:
            if response.status == 200:
                User_ID = (await response.json())["users"][0]["_id"]

                StreamInfo_URL = f"https://api.twitch.tv/kraken/streams/{User_ID}"

                async with request(
                    "GET",
                    StreamInfo_URL,
                    headers={
                        "Client-ID": os.environ.get("twitchclientid"),
                        "Accept": "application/vnd.twitchtv.v5+json",
                    },
                ) as response2:
                    if response2.status == 200:
                        if (await response2.json())["stream"] != None:
                            embed = Embed(
                                title=f"{(await response2.json())['stream']['channel']['display_name']} Stream Info",
                                colour=Colour.dark_purple(),
                                timestamp=datetime.utcnow(),
                            )

                            fields = [
                                (
                                    "Title",
                                    f"{(await response2.json())['stream']['channel']['status']}",
                                    True,
                                ),
                                (
                                    "Game",
                                    f"{(await response2.json())['stream']['channel']['game']}",
                                    True,
                                ),
                            ]

                            for name, value, inline in fields:
                                embed.add_field(name=name, value=value, inline=inline)

                            embed.set_thumbnail(
                                url=(await response2.json())["stream"]["channel"][
                                    "logo"
                                ]
                            )

                            await ctx.reply(embed=embed)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("twitch")


def setup(bot):
    bot.add_cog(Twitch(bot))
