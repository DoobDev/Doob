from discord.ext.commands import Cog, command, BucketType, cooldown
from discord import Embed, Colour

from ..db import db # pylint: disable=relative-beyond-top-level

from aiohttp import request

from datetime import datetime

from typing import Optional

import os
from dotenv import load_dotenv
load_dotenv()

class LastFM(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="lastfm", aliases=["fm"], brief="Get your Last.fm information.")
    @cooldown(1, 5, BucketType.user)
    async def lastfm_lookup_command(self, ctx, *, username: Optional[str]):
        """Request some information on a specific Last.fm User!\n`Username` = Last.fm Username"""
        username = username or db.record("SELECT LastfmUsername FROM exp WHERE UserID = ?", ctx.author.id)[0]

        User_URL = f"https://ws.audioscrobbler.com/2.0/?method=user.getinfo&user={username}&api_key={os.environ.get('lastfmkey')}&format=json"
        async with request("GET", User_URL) as response:
            if response.status == 200:
                data = (await response.json())['user']

                embed=Embed(title=f"{data['name']}'s Last.fm profile")

                embed.set_thumbnail(url=data['image'][3]['#text'])

                await ctx.send(embed=embed)

            else:
                await ctx.send(f"The Last.fm API returned a {response.status} status.")

    @command(name="setlastfm", aliases=["setfm"], brief="Sets your Last.fm username.")
    @cooldown(1, 5, BucketType.user)
    async def set_overwatch_profile(self, ctx, username: Optional[str]):
        """Sets your Last.fm username for `doob/lastfm`"""

        if username != None:
            embed=Embed(title="Setting Last.fm username:", description=username, colour=ctx.author.colour)

            embed.set_thumbnail(url=ctx.author.avatar_url)

            db.execute("UPDATE exp SET LastfmUsername = ? WHERE UserID = ?", username, ctx.author.id)
            db.commit()

            await ctx.send(embed=embed)

        else:
            username =  db.record("SELECT LastfmUsername FROM exp WHERE UserID = ?", ctx.author.id)
            embed=Embed(title="Your Last.fm username", description=username[0], 
                        colour=ctx.author.colour)

            embed.set_thumbnail(url=ctx.author.avatar_url)

            await ctx.send(embed=embed)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("lastfm")

def setup(bot):
	bot.add_cog(LastFM(bot))