import asyncio
from pyosu import OsuApi

from discord.ext.commands import Cog, command, BucketType, cooldown
from discord import Embed, Colour

from ..db import db # pylint: disable=relative-beyond-top-level

from datetime import datetime

from typing import Optional

import os
from dotenv import load_dotenv
load_dotenv()

class osu(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="osu", aliases=["osuprofile"], brief="Get some information about your osu! account!")
    @cooldown(1, 5, BucketType.user)
    async def osu_command(self, ctx, username: Optional[str]):
        username = username or db.record("SELECT osuUsername FROM exp WHERE UserID = ?", ctx.author.id)[0]

        api = OsuApi(os.environ.get('osu_api'))

        user = await api.get_user(user=username, mode=0, type_str='string')

        embed=Embed(title=f"{user.username}'s osu! profile", description=f"https://osu.ppy.sh/u/{user.username}",
                    colour=ctx.author.colour, timestamp=datetime.utcnow())

        fields = [("Play Count", user.playcount, True),
                  ("Rank", user.pp_rank, True),
                  ("Country Rank", user.pp_country_rank, True),
                  ("Total Score", user.total_score, False),
                  ("Accuracy", user.accuracy, False),
                  ("Level", user.level, True),
                  ("Country", user.country, False),
                  ("<:rankingA:779734932519387136> Ranks", user.count_rank_a, True),
                  ("<:rankingS:779734932850343958> Ranks", user.count_rank_s, True),
                  ("<:rankingSd:779734932795686943> Ranks", user.count_rank_sh, True),
                  ("<:rankingSS:779734933178417163> Ranks", user.count_rank_ss, True),
                  ("<:rankingSSd:779734933077884968> Ranks", user.count_rank_ssh, True)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        embed.set_thumbnail(url=f"https://a.ppy.sh/{user.user_id}")

        await ctx.send(embed=embed)
    
    @command(name="setosu", aliases=["setosuusername", 'setosuuser', 'sou'], brief="Set your osu! username!")
    @cooldown(1, 5, BucketType.user)
    async def osu_set_command(self, ctx, username: Optional[str]):
        if username != None:
            embed=Embed(title="Setting osu! username:", description=username, colour=ctx.author.colour)

            embed.set_thumbnail(url=ctx.author.avatar_url)

            db.execute("UPDATE exp SET osuUsername = ? WHERE UserID = ?", username, ctx.author.id)
            db.commit()

            await ctx.send(embed=embed)

        else:
            username =  db.record("SELECT osuUsername FROM exp WHERE UserID = ?", ctx.author.id)
            embed=Embed(title="Your osu! username", description=username[0], 
                        colour=ctx.author.colour)

            embed.set_thumbnail(url=ctx.author.avatar_url)

            await ctx.send(embed=embed)


    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("osu")

def setup(bot):
	bot.add_cog(osu(bot))
