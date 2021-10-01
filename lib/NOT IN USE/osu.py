"""
SADLY PYOSU NO LONGER WORKS (iirc)
"""
import asyncio
from pyosu import OsuApi

from discord.ext.commands import Cog, command, BucketType, cooldown
from discord import Embed, Colour

from ..db import db  # pylint: disable=relative-beyond-top-level

from datetime import datetime

from typing import Optional

import os
from dotenv import load_dotenv

load_dotenv()


class Osu(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(
        name="osu",
        aliases=["osuprofile"],
        brief="Get some information about your osu! account!",
    )
    @cooldown(1, 5, BucketType.user)
    async def osu_command(self, ctx, username: Optional[str]):
        prefix = db.record("SELECT Prefix from guilds WHERE GuildID = ?", ctx.guild.id)

        if (
            db.record("SELECT osuUsername FROM users WHERE UserID = ?", ctx.author.id)[
                0
            ]
            == None
        ):
            await ctx.reply(
                f"Your osu! username is set to None\nSet it to your username by doing `{prefix[0]}setosu`"
            )
            return

        username = (
            username
            or db.record(
                "SELECT osuUsername FROM users WHERE UserID = ?", ctx.author.id
            )[0]
        )

        api = OsuApi(os.environ.get("osu_api"))

        user = await api.get_user(user=username, mode=0, type_str="string")

        embed = Embed(
            title=f"{user.username}'s osu! profile",
            description=f"https://osu.ppy.sh/u/{user.username}",
            colour=ctx.author.colour,
            timestamp=datetime.utcnow(),
        )

        fields = [
            ("Play Count", "{:,}".format(user.playcount), True),
            ("Rank", "{:,}".format(user.pp_rank), True),
            ("Country Rank", "{:,}".format(user.pp_country_rank), True),
            ("Total Score", "{:,}".format(round(user.total_score)), False),
            ("Accuracy", "{:,}".format(round(user.accuracy, 2)), False),
            ("Level", "{:,}".format(round(user.level)), True),
            ("Country", user.country, False),
            (
                "<:rankingA:779734932519387136> Ranks",
                "{:,}".format(user.count_rank_a),
                True,
            ),
            (
                "<:rankingS:779734932850343958> Ranks",
                "{:,}".format(user.count_rank_s),
                True,
            ),
            (
                "<:rankingSd:779734932795686943> Ranks",
                "{:,}".format(user.count_rank_sh),
                True,
            ),
            (
                "<:rankingSS:779734933178417163> Ranks",
                "{:,}".format(user.count_rank_ss),
                True,
            ),
            (
                "<:rankingSSd:779734933077884968> Ranks",
                "{:,}".format(user.count_rank_ssh),
                True,
            ),
        ]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        embed.set_thumbnail(url=f"https://a.ppy.sh/{user.user_id}")

        await ctx.reply(embed=embed)

    @command(
        name="setosu",
        aliases=["setosuusername", "setosuuser", "sou", "osuset"],
        brief="Set your osu! username!",
    )
    @cooldown(1, 5, BucketType.user)
    async def osu_set_command(self, ctx, username: Optional[str]):
        if username != None:
            api = OsuApi(os.environ.get("osu_api"))
            user = await api.get_user(user=username, mode=0, type_str="string")

            embed = Embed(
                title="Setting osu! username:",
                description=username,
                colour=ctx.author.colour,
            )

            embed.set_thumbnail(url=f"https://a.ppy.sh/{user.user_id}")

            db.execute(
                "UPDATE users SET osuUsername = ? WHERE UserID = ?",
                username,
                ctx.author.id,
            )
            db.commit()

            await ctx.reply(embed=embed)

        else:
            username = db.record(
                "SELECT osuUsername FROM users WHERE UserID = ?", ctx.author.id
            )[0]
            api = OsuApi(os.environ.get("osu_api"))
            user = await api.get_user(user=username, mode=0, type_str="string")

            embed = Embed(
                title="Your osu! username",
                description=username,
                colour=ctx.author.colour,
            )

            embed.set_thumbnail(url=f"https://a.ppy.sh/{user.user_id}")

            await ctx.reply(embed=embed)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("osu")


def setup(bot):
    bot.add_cog(Osu(bot))
