from datetime import datetime, timedelta
from random import randint
from typing import Optional

from discord import Member, Embed
from discord.ext.commands import Cog
from discord.ext.commands import command, has_permissions
from discord.ext.menus import MenuPages, ListPageSource
from lib.bot import bot  # pylint: disable=no-name-in-module, import-error
from ..db import db  # pylint: disable=relative-beyond-top-level
import json
import os
from glob import glob

with open("~/doob/lib/cogs/blacklisted_users.json") as blacklisted_users_file:
    BLACKLISTED_USERS = json.load(blacklisted_users_file)


class Exp(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def process_xp(self, message):
        if message.author.id not in BLACKLISTED_USERS["blacklist"]:
            xp, lvl, xplock = db.record(
                "SELECT XP, Level, XPLock FROM users WHERE UserID = ?",
                message.author.id,
            )
            xp_g, lvl_g, xplock_g = db.record(
                "SELECT XP, Level, XPLock FROM guildexp WHERE UserID = ? AND GuildID = ?",
                message.author.id,
                message.guild.id,
            )

            if datetime.utcnow() > datetime.fromisoformat(xplock):
                await self.add_xp(message, xp, lvl)

            if datetime.utcnow() > datetime.fromisoformat(xplock_g):
                await self.add_gxp(message, xp_g, lvl_g)

    async def add_xp(self, message, xp, lvl):
        if message.author.id not in BLACKLISTED_USERS["blacklist"]:
            xp_to_add = randint(10, 20)
            level_up_messages = db.record(
                "SELECT LevelMessages FROM guilds WHERE GuildID = ?", message.guild.id
            )[0]

            new_lvl = int(((xp + xp_to_add) // 42) ** 0.55)

            db.execute(
                "UPDATE users SET XP = XP + ?, Level = ?, XPLock = ? WHERE UserID = ?",
                xp_to_add,
                new_lvl,
                (datetime.utcnow() + timedelta(seconds=50)).isoformat(),
                message.author.id,
            )

            if new_lvl > lvl and level_up_messages in ["yes", "Yes"]:
                await message.channel.send(
                    f"{message.author.mention} leveled up to {new_lvl:,}!",
                    delete_after=10,
                )

    async def add_gxp(self, message, xp, lvl):
        if message.author.id not in BLACKLISTED_USERS["blacklist"]:
            xp_to_add = randint(10, 20)
            level_up_messages = db.record(
                "SELECT LevelMessages FROM guilds WHERE GuildID = ?", message.guild.id
            )[0]

            new_lvl = int(((xp + xp_to_add) // 42) ** 0.55)

            db.execute(
                f"UPDATE guildexp SET XP = XP + ?, Level = ?, XPLock = ? WHERE UserID = ? AND GuildID = ?",
                xp_to_add,
                new_lvl,
                (datetime.utcnow() + timedelta(seconds=50)).isoformat(),
                message.author.id,
                message.guild.id,
            )
            db.commit()

            if new_lvl > lvl and level_up_messages in ["yes", "Yes"]:
                await message.channel.send(
                    f"{message.author.mention} leveled up to server level {new_lvl:,}!",
                    delete_after=10,
                )

    @command(name="level", aliases=["rank", "lvl"], brief="Shows your level, and rank.")
    async def display_level(self, ctx, target: Optional[Member]):
        """Shows your Global+Server Doob level, rank and XP!"""
        target = target or ctx.author

        ids = db.column("SELECT UserID FROM users ORDER BY XP DESC")
        ids_g = db.column(
            "SELECT UserID from guildexp WHERE GuildID = (?) ORDER BY XP DESC",
            ctx.guild.id,
        )
        # ids_g = db.column("SELECT UserID FROM users ORDER BY XP DESC WHERE GuildID = ?", ctx.guild.id)
        xp, lvl = db.record(
            "SELECT XP, Level FROM users WHERE UserID = ?", target.id
        ) or (None, None)
        xp_g, lvl_g = (
            db.record(
                "SELECT XP, Level FROM guildexp WHERE (UserID, GuildID) = (?, ?)",
                target.id,
                ctx.guild.id,
            )
            or (None, None)
        )

        if lvl is not None:
            to_next_level = int((lvl + 1) ** (20 / 11) * 42) - xp
            embed = Embed(
                title=f"{target.display_name} is level {lvl:,}",
                description=f"XP: {xp:,}\nXP to next level {to_next_level:,}"
                + f"\n\nServer XP: {xp_g:,}\nServer level: {lvl_g:,}",
                colour=ctx.author.color,
            )

            fields = [
                ("Global Rank:", f"{ids.index(target.id)+1:,} of {len(ids):,}", False),
                (
                    f"Server Rank:",
                    f"{ids_g.index(target.id)+1:,} of {len(ids_g):,}",
                    False,
                ),
            ]

            for field in fields:
                embed.add_field(name=field[0], value=field[1], inline=field[2])

            embed.set_thumbnail(url=target.avatar_url)

            await ctx.send(embed=embed)

        else:
            ctx.send("That member is not in the XP Database.")

    @command(
        name="levelmessages",
        aliases=["slm", "lm", "setlevelmessages"],
        brief="Set the server's level messages",
    )
    @has_permissions(manage_guild=True)
    async def set_level_messages(self, ctx, *, yes_or_no: Optional[str]):
        """PLEASE, put 'yes' if you DO want level messages\n`Manage Server` permission required."""
        levelmessages = db.records(
            "SELECT LevelMessages FROM guilds WHERE GuildID = ?", ctx.guild.id
        ) or (None)
        prefix = db.records("SELECT Prefix FROM guilds WHERE GuildID = ?", ctx.guild.id)

        if yes_or_no in ["Yes", "yes", "no", "No"]:
            db.execute(
                "UPDATE guilds SET LevelMessages = ? WHERE GuildID = ?",
                yes_or_no,
                ctx.guild.id,
            )
            db.commit()
            await ctx.send(f"Level messages set to `{yes_or_no}`.")

        else:
            await ctx.send(
                f"The current setting for Level Messages is: `{levelmessages[0][0]}`\nTo change it, type `{prefix[0][0]}levelmessages (yes or no)`"
            )

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("exp")

    @Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            await self.process_xp(message)


def setup(bot):
    bot.add_cog(Exp(bot))
