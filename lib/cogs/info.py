from datetime import datetime

from typing import Optional

from discord import Embed, Member
from discord.ext.commands import Cog, command, cooldown, BucketType
from discord.utils import get

from discord_slash.utils.manage_commands import create_option
from discord_slash import cog_ext

from ..db import db  # pylint: disable=relative-beyond-top-level

import json
import os

with open("config.json") as config_file:
    config = json.load(config_file)

absolute_path = os.path.dirname(os.path.abspath(__file__))
# Or: file_path = os.path.join(absolute_path, 'folder', 'my_file.py')


def get_path(filename):
    return absolute_path + f"/{filename}.json"


def read_json(filename):
    with open(get_path(filename), "r") as file:
        data = json.load(file)
    return data


BLACKLISTED_USERS = read_json("blacklisted_users")

class Info(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def user_info(self, ctx, target, patreon_status, blacklisted):
        ids = db.column("SELECT UserID FROM users ORDER BY XP DESC")
        xp, lvl = db.record(
            "SELECT XP, Level FROM users WHERE UserID = ?", target.id
        ) or (None, None)
        warnings = db.records(
            f"SELECT Warns FROM warns WHERE UserID = {target.id} AND GuildID = {ctx.guild.id}"
        )[0][0]
        globalwarns = db.records(f"SELECT Warns FROM warns WHERE UserID = {target.id}")[
            0
        ][0]

        embed = Embed(
            title=f"{target.name}'s info",
            colour=target.colour,
            timestamp=datetime.utcnow(),
        )

        patreon = "Yes" if patreon_status == True else "No"
        fields = [
            ("Username", target.mention, True),
            ("ID", target.id, True),
            ("Doob Global XP", xp, False),
            ("Doob Global Level", lvl, True),
            (
                "Doob Global Rank",
                f"{ids.index(target.id)+1} of {len(ids):,} users globally.",
                True,
            ),
            ("Warnings (Server)", warnings, False),
            ("Warnings (Global)", globalwarns, True),
            ("Bot", target.bot, False),
            ("Top role", target.top_role.mention, True),
            ("Status", str(target.status).title(), True),
            (
                "Activity",
                f"{str(target.activity.type).split('.')[-1].title() if target.activity else 'N/A'} - {target.activity.name if target.activity else ''}",
                True,
            ),
            (
                "Account creation date",
                target.created_at.strftime("%m/%d/%Y %H:%M;%S"),
                True,
            ),
            (
                "Joined the server at",
                target.joined_at.strftime("%m/%d/%Y %H:%M;%S"),
                True,
            ),
            ("Boosted this server", bool(target.premium_since), True),
            ("Patron of Doob?", patreon, True),
        ]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        if blacklisted is True:
            embed.add_field(name="Blacklisted?", value="✅ This user has been blacklisted from using Doob.", inline=False)
        else:
            embed.add_field(name="Blacklisted?", value="❌ This user is not blacklisted from using Doob.", inline=False)

        embed.set_thumbnail(url=target.avatar_url)
        await ctx.send(embed=embed)

    @command(
        name="userinfo",
        aliases=["member", "user", "profile", "ui", "whois"],
        brief="Gives info about a specific user.",
    )
    @cooldown(1, 10, BucketType.user)
    async def user_info_command(self, ctx, target: Optional[Member]):
        """Gives you info about a user."""
        target = target or ctx.author

        homeGuild = self.bot.get_guild(config["homeGuild_id"])  # Support Server ID.
        patreonRole = get(
            homeGuild.roles, id=config["patreonRole_id"]
        )  # Patreon role ID.

        member = []

        for pledger in homeGuild.members:
            if pledger == target:
                member = pledger

        if target in homeGuild.members and patreonRole in member.roles:
            patreon_status = True
            blacklisted = target.id in BLACKLISTED_USERS["blacklist"]
            await self.user_info(ctx, target, patreon_status, blacklisted)

        elif target.id in BLACKLISTED_USERS["blacklist"] and target not in homeGuild.members and patreonRole in member.roles:
            blacklisted = True
            await self.user_info(ctx, target, False, blacklisted)

        else:
            await self.user_info(ctx, target, patreon_status=False, blacklisted=False)

    @cog_ext.cog_slash(
        name="userinfo",
        description="Gives you info about a user.",
        options=[
            create_option(
                name="target",
                description="User you would like to recieve info on.",
                option_type=6,
                required=True,
            )
        ],
    )
    async def user_info_slash(self, ctx, target: Optional[Member]):
        homeGuild = self.bot.get_guild(config["homeGuild_id"])  # Support Server ID.
        patreonRole = get(
            homeGuild.roles, id=config["patreonRole_id"]
        )  # Patreon role ID.

        member = []

        for pledger in homeGuild.members:
            if pledger == target:
                member = pledger

        if target in homeGuild.members and patreonRole in member.roles:
            patreon_status = True
            blacklisted = target.id in BLACKLISTED_USERS["blacklist"]
            await self.user_info(ctx, target, patreon_status, blacklisted)

        elif target.id in BLACKLISTED_USERS["blacklist"]:
            blacklisted = True
            await self.user_info(ctx, target, False, blacklisted)

        else:
            await self.user_info(ctx, target, patreon_status=False, blacklisted=False)

    async def server_info(self, ctx, banned_members):
        embed = Embed(
            title="Server's info",
            colour=ctx.guild.owner.colour,
            timestamp=datetime.utcnow(),
        )

        # statuses = [
        #    len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
        #    len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
        #    len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
        #    len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members))),
        # ]

        fields = [
            ("ID", ctx.guild.id, True),
            ("Owner", ctx.guild.owner, True),
            ("Region", ctx.guild.region, True),
            ("Created at", ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
            ("Members", len(ctx.guild.members), True),
            ("Humans", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
            ("Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
            # (
            #    "Statuses",
            #    f"🟢 {statuses[0]} 🟠 {statuses[1]} 🔴 {statuses[2]} ⚪ {statuses[3]}",
            #    True,
            # ),
            ("Text channels", len(ctx.guild.text_channels), True),
            ("Voice channels", len(ctx.guild.voice_channels), True),
            ("Categories", len(ctx.guild.categories), True),
            ("Roles", len(ctx.guild.roles), True),
            ("\u200b", "\u200b", True),
        ]

        embed.set_thumbnail(url=ctx.guild.icon_url)

        if ctx.guild.banner:
            embed.set_image(url=ctx.guild.banner_url)

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        if banned_members == True:
            embed.add_field(
                name="Banned members", value=len(await ctx.guild.bans()), inline=True
            )
        await ctx.send(embed=embed)

    @command(
        name="serverinfo",
        aliases=["guildinfo", "gi", "si"],
        brief="Gives info about the server.",
    )
    @cooldown(1, 10, BucketType.user)
    async def server_info_command(self, ctx):
        """Gives you info about the server the command is executed in."""
        if ctx.guild.me.guild_permissions.administrator == True:
            await self.server_info(ctx, banned_members=True)

        else:
            await self.server_info(ctx, banned_members=False)

    @cog_ext.cog_slash(
        name="serverinfo",
        description="Gives you info about your server.",
    )
    async def server_info_slash_command(self, ctx):
        if ctx.guild.me.guild_permissions.administrator == True:
            await self.server_info(ctx, banned_members=True)

        else:
            await self.server_info(ctx, banned_members=False)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("info")


def setup(bot):
    bot.add_cog(Info(bot))
