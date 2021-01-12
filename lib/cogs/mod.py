from datetime import datetime, timedelta
from typing import Optional
from random import randint

from discord.utils import find
from discord import Embed, Member, Role, TextChannel, NotFound, Object
from discord.ext.commands import (
    command,
    has_permissions,
    bot_has_permissions,
    Cog,
    Greedy,
    Converter,
    CheckFailure,
    BadArgument,
    BucketType,
    cooldown,
)

from ..db import db  # pylint: disable=relative-beyond-top-level


class BannedUser(Converter):
    async def convert(self, ctx, arg):
        if ctx.guild.me.guild_permissions.ban_members:
            if arg.isdigit():
                try:
                    return (await ctx.guild.fetch_ban(Object(id=int(arg)))).user

                except NotFound:
                    raise BadArgument

        banned = [e.user for e in await ctx.guild.bans()]
        if banned:
            if (user := find(lambda u: str(u) == arg, banned)) is not None:
                return user

            else:
                raise BadArgument


class Mod(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(
        name="kick", aliases=["k", "kickmember"], brief="Kick a member from the server."
    )
    @bot_has_permissions(kick_members=True)
    @has_permissions(kick_members=True)
    async def kick_command(
        self,
        ctx,
        targets: Greedy[Member],
        *,
        reason: Optional[str] = "No reason provided.",
    ):
        """Kicks a member from the server.\n`Kick Members` permission required."""
        if not len(targets):
            await ctx.reply("One or more required arguments are missing.")

        else:
            for target in targets:
                if (
                    ctx.guild.me.top_role.position != target.top_role.position
                    and ctx.author.top_role.position > target.top_role.position
                ):

                    await target.kick(reason=reason)
                    await ctx.reply("Member Kicked.")
                else:
                    await ctx.reply(
                        "Something went wrong.\nYou might not be able to kick that member."
                    )

    @kick_command.error
    async def kick_command_error(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.reply("Insufficient permissions to perform that task.")

    async def mute_members(self, message, targets, reason):
        unmutes = []
        mute_role = db.field(
            "SELECT MutedRole FROM guilds WHERE GuildID = ?", message.guild.id
        )
        comma = ", "
        tNames = []
        for target in targets:
            tNames.append(f"{target.display_name}")
        for target in targets:
            mutedrole = message.guild.get_role(int(mute_role))
            if not mutedrole in target.roles:
                role_ids = ",".join([str(r.id) for r in target.roles])
                await target.edit(roles=[mutedrole])
                db.execute(
                    "INSERT INTO mutes VALUES (?, ?, ?)",
                    target.id,
                    message.guild.id,
                    role_ids,
                )
                db.commit()

        embed = Embed(title="Muted:", description=f"{comma.join(tNames)}")
        await message.channel.send(embed=embed)

        return unmutes

    @command(
        name="mute", aliases=["m", "silence"], brief="Mutes a member from the server."
    )
    @bot_has_permissions(manage_roles=True)
    @has_permissions(manage_roles=True)
    async def mute_command(
        self,
        ctx,
        targets: Greedy[Member],
        *,
        reason: Optional[str] = "No reason provided.",
    ):
        """Mutes a member from the server\nRequires the `Manage Roles` permission"""
        if not len(targets):
            await ctx.reply("One or more required arguments are missing.")

        else:
            unmutes = await self.mute_members(ctx.message, targets, reason)

            if len(unmutes):
                mute_role = db.field(
                    "SELECT MutedRole FROM guilds WHERE GuildID = ?", ctx.guild.id
                )
                TheRole = ctx.guild.get_role(int(mute_role))
                for target in targets:
                    await target.remove_roles(TheRole)
                    db.execute(
                        f"DELETE FROM mutes WHERE UserID = {target.id} AND GuildID = {ctx.guild.id}"
                    )
                    db.commit()
                    await ctx.reply("Unmuted! <:PogU:560267624966258690>")

    @command(name="unmute", aliases=["um"], brief="Unmutes a member from the server.")
    @bot_has_permissions(manage_roles=True)
    @has_permissions(manage_roles=True)
    async def delmute_command(self, ctx, targets: Greedy[Member]):
        """Unmutes a member from the server\nRequires the `Manage Roles` permission"""
        comma = ", "
        tNames = []
        for target in targets:
            tNames.append(f"{target.display_name}")
        for target in targets:
            role_ids = db.field(
                f"SELECT RoleIDs FROM mutes WHERE UserID = {target.id} AND GuildID = {ctx.guild.id}"
            )
            roles = [
                ctx.guild.get_role(int(id_)) for id_ in role_ids.split(",") if len(id_)
            ]
            await target.edit(roles=roles)
            db.execute(
                f"DELETE FROM mutes WHERE UserID = {target.id} AND GuildID = {ctx.guild.id}"
            )
            db.commit()
            target_embed += f" {target.display_name},"

        embed = Embed(title="Unmuted:", description=f"{comma.join(tNames)}")
        await ctx.reply(embed=embed)

    @mute_command.error
    async def mute_command_error(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.reply("Insufficient permissions to perform that task.")

    @command(
        name="ban", aliases=["b", "banmember"], brief="Ban a member from the server."
    )
    @bot_has_permissions(ban_members=True)
    @has_permissions(ban_members=True)
    async def ban_command(
        self,
        ctx,
        targets: Greedy[Member],
        *,
        reason: Optional[str] = "No reason provided.",
    ):
        """Bans a member from the server\n`Ban Members` permission required."""
        if not len(targets):
            await ctx.reply("One or more required arguments are missing.")

        else:
            for target in targets:
                if (
                    ctx.guild.me.top_role.position != target.top_role.position
                    and ctx.author.top_role.position > target.top_role.position
                ):

                    await target.ban(reason=reason)
                    await ctx.reply("Member banned.")

                else:
                    await ctx.reply(
                        "Something went wrong.\nYou might not be able to ban that member."
                    )

    @ban_command.error
    async def ban_command_error(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.reply("Insufficient permissions to perform that task.")

    @command(
        name="russianroulette",
        aliases=["banroulette", "luckyban", "rr"],
        brief="If you don't survive the roulette, you get banned!",
    )
    @has_permissions(ban_members=True)
    @cooldown(1, 30, BucketType.guild)
    async def russian_roulette_command(self, ctx, targets: Greedy[Member]):
        """1/6 Chance to get banned, good luck have fun.\n`Ban Members` permission required."""
        for target in targets:
            roll = randint(1, 7)

            if roll == 1:
                if not len(targets):
                    await ctx.reply("One or more required arguments are missing.")

                else:
                    for target in targets:
                        if (
                            ctx.guild.me.top_role.position != target.top_role.position
                            and ctx.author.top_role.position > target.top_role.position
                        ):

                            await target.ban(
                                reason="They couldn't survive russian roulette."
                            )
                            await ctx.reply(
                                f"{target.display_name} [`{target.id}`] will (or will not) be missed."
                            )

                        else:
                            await ctx.reply(
                                "Something went wrong.\nYou might not be able to ban that member.\nYou survived this one..."
                            )

            else:
                for target in targets:
                    await ctx.reply(
                        f"{target.display_name} [`{target.id}`] survived.\n(rolled a `{roll}`, needs to hit a `1` to get banned.)"
                    )

    @command(name="unban", aliases=["pardon"])
    @bot_has_permissions(ban_members=True)
    @has_permissions(ban_members=True)
    async def unban_command(
        self,
        ctx,
        targets: Greedy[BannedUser],
        *,
        reason: Optional[str] = "No reason provided.",
    ):
        if not len(targets):
            await ctx.reply("One or more required arguments are missing.")

        else:
            for target in targets:
                await ctx.guild.unban(target, reason=reason)
                await ctx.reply("Member unbanned.")

    @command(
        name="clear", aliases=["purge"], brief="Clears amount of messages provided."
    )
    @bot_has_permissions(manage_messages=True)
    @has_permissions(manage_messages=True)
    async def clear_messages(
        self, ctx, targets: Greedy[Member], limit: Optional[int] = 1
    ):
        """Clears an ammount of messages provided by the user.\n`Manage Messages` permission required."""

        def _check(message):
            return not len(targets) or message.author in targets

        if 0 < limit <= 100:
            with ctx.channel.typing():
                await ctx.message.delete()
                deleted = await ctx.channel.purge(
                    limit=limit,
                    after=datetime.utcnow() - timedelta(days=14),
                    check=_check,
                )

                await ctx.send(f"Deleted {len(deleted):,} messages.", delete_after=10)

        else:
            await ctx.reply("The limit provided is not within acceptable bounds.")

    @command(
        name="setlogchannel",
        aliases=["slc", "logchannel", "setlog", "setlogs"],
        brief="Set the server's log channel.",
    )
    @has_permissions(manage_guild=True)
    async def set_log_channel(self, ctx, *, channel: Optional[TextChannel]):
        """Sets the logging channel for the server.\n`Manage Server` permission required."""
        current_channel = db.records(
            "SELECT LogChannel FROM guilds WHERE GuildID = ?", ctx.guild.id
        )
        prefix = db.records("SELECT Prefix from guilds WHERE GuildID = ?", ctx.guild.id)

        if channel == None:
            await ctx.reply(
                f"The current setting for the Log Channel is currently: <#{current_channel[0][0]}>\nTo change it, type `{prefix[0][0]}setlogchannel #<log channel>`"
            )

        else:
            db.execute(
                "UPDATE guilds SET LogChannel = ? WHERE GuildID = ?",
                str(channel.id),
                ctx.guild.id,
            )
            db.commit()
            await ctx.reply(f"Log channel set to <#{channel.id}>")

    @command(
        name="setstarboardchannel",
        aliases=["ssbc", "starboardchannel", "setstar", "setstarboard"],
        brief="Set the server's starboard channel.",
    )
    @has_permissions(manage_guild=True)
    async def set_starboard_channel(self, ctx, *, channel: Optional[TextChannel]):
        """Sets the starboard channel for the server.\n`Manage Server` permission required."""
        current_channel = db.records(
            "SELECT StarBoardChannel FROM guilds WHERE GuildID = ?", ctx.guild.id
        )
        prefix = db.records("SELECT Prefix from guilds WHERE GuildID = ?", ctx.guild.id)

        if channel == None:
            await ctx.reply(
                f"The current setting for the StarBoard Channel is currently: <#{current_channel[0][0]}>\nTo change it, type `{prefix[0][0]}setstarboardchannel #<starboard channel>`"
            )

        else:
            db.execute(
                "UPDATE guilds SET StarBoardChannel = ? WHERE GuildID = ?",
                str(channel.id),
                ctx.guild.id,
            )
            db.commit()
            await ctx.reply(f"StarBoard channel set to <#{channel.id}>")

    @command(
        name="setmuterole",
        aliases=["smr", "muterole", "setmute"],
        brief="Set the server's mute role.",
    )
    @has_permissions(manage_guild=True)
    async def set_mute_role(self, ctx, *, role: Optional[Role]):
        """Sets the `Muted` role for your server.\n`Manage Server` premission required."""
        cur_role = db.records(
            "SELECT MutedRole FROM guilds WHERE GuildID = ?", ctx.guild.id
        )
        prefix = db.records("SELECT Prefix from guilds WHERE GuildID = ?", ctx.guild.id)

        if ctx.guild.me.top_role.position > role.position:
            db.execute(
                "UPDATE guilds SET MutedRole = ? WHERE GuildID = ?",
                str(role.id),
                ctx.guild.id,
            )
            db.commit()
            await ctx.reply(f"Mute role set to `{role}`")

        else:
            await ctx.reply(
                f"Please try a different role.\nYou may need to move the `Doob` role in your server settings above the `{role}` role."
            )

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("mod")


def setup(bot):
    bot.add_cog(Mod(bot))
