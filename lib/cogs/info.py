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


def get_path(filename):
    return absolute_path + f"/{filename}.json"


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

        def get_warning_emote():
            if warnings > 3:
                return "<:Dwarningneg:869815366803668992>"

            elif warnings > 0:
                return "<:Dwarning:869830849061879859>"

            else:
                return "<:Dwarningpos:869815366715584513>"

        def get_global_warn_emote():
            if globalwarns > 3:
                return "<:Dwarningneg:869815366803668992>"

            elif globalwarns > 0:
                return "<:Dwarning:869830849061879859>"

            else:
                return "<:Dwarningpos:869815366715584513>"

        def get_bot_emote():
            if target.bot:
                return "<:Dbot:869815359652397076>"
            else:
                return "<:Dbotpink:869815365071413258>"

        def get_blacklisted_emote():
            if blacklisted is True:
                return "<:Dcrossneg:869815364383572059>"
            else:
                return "<:Dcrosspos:869815366002556928>"

        roles = []

        for role in target.roles:
            if role.name == "@everyone":
                role.name = " "
                roles.append(role.name)
            else:
                roles.append(f"{role.mention}")

        roles_list = (
            "\n<:Dspace:869830848743092247> <:DRightTrans:869842970415890432> ".join(
                roles
            )
        )

        patreon = "Yes" if patreon_status == True else "No"

        desc = f"""<:Dusernuetral:869830849380646922> **Username:** {target.mention}
        <:Dspace:869830848743092247> <:DRightTrans:869842970415890432> **ID:** {target.id}
        <:Dclockpink:869815366816239666> **Created:** <t:{int(datetime.replace(target.created_at).timestamp())}:R>
        <:Dspace:869830848743092247> <:DRightTrans:869842970415890432> **Joined:** <t:{int(datetime.replace(target.joined_at).timestamp())}:R>
        \n{get_warning_emote()} **Warnings (Server):** {warnings}
        <:Dspace:869830848743092247> {get_global_warn_emote()} ** Warnings (Global):** {globalwarns}
        \n{get_bot_emote()} **Bot**: {target.bot}
        <:Dstarpink:869815366539419648> **Booster:** {bool(target.premium_since)}
        \n<:Dstarpink:869815366539419648> **XP:** {xp}
        <:Dspace:869830848743092247> <:DRightTrans:869842970415890432> **Level:** {lvl}
        \n<:Dheart:869815366132576286> **Doob+ Member?** {patreon}
        \n{get_blacklisted_emote()} **Blacklisted?** {bool(blacklisted)}
        \n<:Dmisc:869815363276243006> **Roles:** {roles_list}"""

        embed = Embed(
            colour=target.colour, timestamp=datetime.utcnow(), description=desc
        )

        embed.set_thumbnail(url=target.avatar_url)

        embed.set_footer(
            text=f"{target.display_name}'s information.", icon_url=target.avatar_url
        )

        await ctx.send(embed=embed)

    @command(
        name="userinfo",
        aliases=["member", "user", "profile", "ui", "whois"],
        brief="Gives info about a specific user.",
    )
    @cooldown(1, 10, BucketType.user)
    async def user_info_command(self, ctx, target: Optional[Member]):
        """Gives you info about a user."""

        def read_json(filename):
            with open(get_path(filename), "r") as file:
                data = json.load(file)
            return data

        BLACKLISTED_USERS = read_json("blacklisted_users")

        target = target or ctx.author

        homeGuild = self.bot.get_guild(config["homeGuild_id"])  # Support Server ID.
        patreonRole = get(
            homeGuild.roles, id=config["patreonRole_id"]
        )  # Patreon role ID.

        member = []

        for pledger in homeGuild.members:
            if pledger == target:
                member = pledger

        blacklisted = target.id in BLACKLISTED_USERS["blacklist"]
        if target in homeGuild.members and patreonRole in member.roles:
            patreon_status = True
            await self.user_info(ctx, target, patreon_status, blacklisted)

        else:
            await self.user_info(
                ctx, target, patreon_status=False, blacklisted=blacklisted
            )

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
        def read_json(filename):
            with open(get_path(filename), "r") as file:
                data = json.load(file)
            return data

        BLACKLISTED_USERS = read_json("blacklisted_users")

        homeGuild = self.bot.get_guild(config["homeGuild_id"])  # Support Server ID.
        patreonRole = get(
            homeGuild.roles, id=config["patreonRole_id"]
        )  # Patreon role ID.

        member = []

        for pledger in homeGuild.members:
            if pledger == target:
                member = pledger

        blacklisted = target.id in BLACKLISTED_USERS["blacklist"]
        if target in homeGuild.members and patreonRole in member.roles:
            patreon_status = True
            await self.user_info(ctx, target, patreon_status, blacklisted)

        else:
            await self.user_info(
                ctx, target, patreon_status=False, blacklisted=blacklisted
            )

    async def server_info(self, ctx, banned_members):
        prefix = db.field("SELECT Prefix FROM guilds WHERE GuildID = ?", ctx.guild.id)

        desc = f"""<:Dusernuetral:869830849380646922> **Name:** {ctx.guild.name}
        <:Dspace:869830848743092247> <:DRightTrans:869842970415890432> **ID:** {ctx.guild.id}
        \n<:Dusernuetral:869830849380646922> **Owner:** {ctx.guild.owner}
        <:Dspace:869830848743092247> <:DRightTrans:869842970415890432> **Owner's ID:** {ctx.guild.owner.id}
        \n<:Dmappink:869815364731678762> **Region:** {ctx.guild.region}
        \n<:Dclockpink:869815366816239666> **Created:** <t:{int(datetime.replace(ctx.guild.created_at).timestamp())}:R>
        \n<:Dusernuetral:869830849380646922> **Members:** {len(ctx.guild.members)}
        <:Dspace:869830848743092247> <:DRightTrans:869842970415890432> **Humans:** {len(list(filter(lambda m: not m.bot, ctx.guild.members)))}
        <:Dspace:869830848743092247> <:DRightTrans:869842970415890432> **Bots:** {len(list(filter(lambda m: m.bot, ctx.guild.members)))}
        \n <:Dmisc:869815363276243006> **Channels:** {len(ctx.guild.channels)}
        <:Dspace:869830848743092247> <:DRightTrans:869842970415890432> **Text channels:** {len(ctx.guild.text_channels)}
        <:Dspace:869830848743092247> <:DRightTrans:869842970415890432> **Voice channels** {len(ctx.guild.voice_channels)}
        <:Dspace:869830848743092247> <:DRightTrans:869842970415890432> **Categories** {len(ctx.guild.categories)}
        \n<:Dmisc:869815363276243006> **Roles:** {len(ctx.guild.roles)}
        <:Dspace:869830848743092247> <:DRightTrans:869842970415890432> **View all of them by doing {prefix}roles**"""

        if banned_members:
            desc += f"\n\n<:DAccessDenied:869815358758985779> **Banned Members:** {len(await ctx.guild.bans())}"

        embed = Embed(
            colour=ctx.guild.owner.colour, timestamp=datetime.utcnow(), description=desc
        )

        embed.set_thumbnail(url=ctx.guild.icon_url)

        if ctx.guild.banner:
            embed.set_image(url=ctx.guild.banner_url)

        embed.set_footer(
            text=f"{ctx.guild.name}'s information", icon_url=ctx.guild.icon_url
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
