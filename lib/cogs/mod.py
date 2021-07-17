from datetime import datetime, timedelta
from typing import Optional
from random import randint
from discord.channel import VoiceChannel

from discord.utils import find
from discord import (
    Embed,
    Member,
    Role,
    TextChannel,
    NotFound,
    Object,
    Colour,
    Permissions,
)
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
    group,
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

    async def mute_members(self, message, targets, reason):
        mute_role = db.field(
            "SELECT MutedRole FROM guilds WHERE GuildID = ?", message.guild.id
        )
        comma = ", "
        tNames = [f"{target.display_name}" for target in targets]
        for target in targets:
            mutedrole = message.guild.get_role(int(mute_role))
            if mutedrole not in target.roles:
                role_ids = ",".join(str(r.id) for r in target.roles)
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

        return []

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
        tNames = [f"{target.display_name}" for target in targets]
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
            target_embed = ""
            target_embed += f" {target.display_name},"

        embed = Embed(title="Unmuted:", description=f"{comma.join(tNames)}")
        await ctx.reply(embed=embed)

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

        if channel is None:
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

        if channel is None:
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

    @command(
        name="createtextchannel",
        aliases=["ctc", "textchannel"],
        brief="Create a text channel.",
    )
    @has_permissions(manage_channels=True)
    async def create_text_channel_command(self, ctx, name: str):
        """Create a text channel in the guild the command was executed in.\n`Manage Server` permission required."""
        channel = await ctx.guild.create_text_channel(name)

        await ctx.send(f"Your Text Channel has been created.\n<#{channel.id}>")

    @command(name="deletetextchannel", aliases=["dtc", "deletetc"], brief="Delete a text channel.")
    @has_permissions(manage_channels=True)
    async def delete_text_channel_command(self, ctx, channel: TextChannel):
        channel = self.bot.get_channel(channel.id)

        await channel.delete()

        await ctx.send(f"Your Text Channel ({channel.name}: `{channel.id}`) has been deleted.")

    @command(
        name="createvoicechannel",
        aliases=["cvc", "voicechannel"],
        brief="Create a voice channel.",
    )
    @has_permissions(manage_channels=True)
    async def create_voice_channel_command(self, ctx, name: str):
        """Create a voice channel in the guild the command was executed in.\n`Manage Server` permission required."""
        channel = await ctx.guild.create_voice_channel(name)

        invite = await channel.create_invite(
            reason="Made using the create voice channel command."
        )

        await ctx.send(f"Your Voice Channel has been created.\n{invite}")

    @command(name="deletevoicechannel", aliases=["dvc", "deletevoice", "deletevc"], brief="Delete a voice channel.")
    @has_permissions(manage_channels=True)
    async def delete_voice_channel_command(self, ctx, channel: VoiceChannel):
        channel = self.bot.get_channel(channel.id)

        await channel.delete()

        await ctx.send(f"The voice channel ({channel.name}: `{channel.id}`) has been deleted.")

    @command(name="warn", aliases=["w"], brief="Warn a user.")
    @has_permissions(manage_guild=True)
    async def warn_command(
        self, ctx, targets: Greedy[Member], *, reason: Optional[str]
    ):
        comma = ", "
        tNames = [f"{target.display_name}" for target in targets]
        for target in targets:
            user = self.bot.get_user(target.id)
            warns = db.records(
                f"SELECT Warns FROM warns WHERE UserID = {target.id} AND GuildID = {ctx.guild.id}"
            )[0][0]
            globalwarns = db.records(
                f"SELECT Warns FROM globalwarns WHERE UserID = {target.id}"
            )[0][0]

            db.execute(
                "UPDATE warns SET warns = ? WHERE UserID = ? AND GuildID = ?",
                warns + 1,
                target.id,
                ctx.guild.id,
            )
            db.execute(
                "UPDATE globalwarns SET warns = ? WHERE UserID = ?",
                globalwarns + 1,
                target.id,
            )
            db.commit()

            if reason is None:
                await user.send(
                    f"🔸 You have been warned in {ctx.guild.name} for no reason."
                )

            else:
                await user.send(
                    f"🔸 You have been warned in {ctx.guild.name} for {reason}"
                )

        await ctx.reply(f"Done!\nWarned: {comma.join(tNames)}")

    @command(
        name="warnings",
        aliases=["warns"],
        brief="See your warnings in the current server, and across all servers.",
    )
    @cooldown(1, 5, BucketType.user)
    async def show_warnings_command(self, ctx):
        warns = db.records(
            f"SELECT Warns FROM warns WHERE UserID = {ctx.author.id} AND GuildID = {ctx.guild.id}"
        )[0][0]
        globalwarns = db.records(
            f"SELECT Warns from globalwarns WHERE UserID = {ctx.author.id}"
        )[0][0]

        embed = Embed(
            title=f"Warnings for {ctx.author.display_name}", colour=ctx.author.colour
        )

        fields = [
            ("This server", warns, False),
            ("Globally across all servers*", globalwarns, False),
        ]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        embed.set_footer(
            text="*Warnings globally across all server with Doob, using Doob's warnings.",
            icon_url=ctx.author.avatar_url,
        )
        embed.set_thumbnail(url=ctx.author.avatar_url)

        await ctx.reply(embed=embed)

    @group(name="role", aliases=["roles"], brief="Manage or see roles in your server.")
    @has_permissions(manage_roles=True)
    async def role(self, ctx):
        if ctx.invoked_subcommand is not None:
            return

        comma = ",\n"
        tNames = []

        for roles in ctx.guild.roles:
            if roles.name == "@everyone":
                tNames.append("@everyone")
            else:
                tNames.append(f"{roles.mention}")

        embed = Embed(
            title=f"Roles in {ctx.guild.name}",
            description=comma.join(tNames),
            colour=ctx.author.colour,
        )

        embed.set_thumbnail(url=ctx.guild.icon_url)

        await ctx.reply(embed=embed)

    @role.command(
        name="-add", aliases=["-a"], brief="Add a role to a user (or multiple)."
    )
    @has_permissions(manage_roles=True)
    async def add_role_command(self, ctx, targets: Greedy[Member], roles: Greedy[Role]):
        comma = ", "
        for target in targets:
            for role in roles:
                await target.add_roles(role)

        tNames = [f"{target.mention}" for target in targets]
        tNames2 = [f"{role.mention}" for role in roles]

        embed = Embed(title="Added roles", colour=Colour.green())

        fields = [
            ("Members:", comma.join(tNames), False),
            ("Roles:", comma.join(tNames2), False),
        ]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.reply(embed=embed)

    @command(name="welcomebackxander", hidden=True)
    async def give_xander_roles_back_command(self, ctx, target: Member):
        roles = [
            726514196552089671,
            829189173646065704,
            825217691837005854,
            721516128920141825,
            721516128928661558,
            794035412007387137,
            737536240861184101,
        ]

        for role in roles:
            await target.add_roles(ctx.guild.get_role(role))

        await ctx.send("Xander!!!!!!!!!!!!!!!!!!!!")

    @role.command(
        name="-remove", aliases=["-r"], brief="Remove a role from a user (or multiple)."
    )
    @has_permissions(manage_roles=True)
    async def remove_role_command(
        self, ctx, targets: Greedy[Member], roles: Greedy[Role]
    ):
        comma = ", "
        for target in targets:
            for role in roles:
                await target.remove_roles(role)

        tNames = [f"{target.mention}" for target in targets]
        tNames2 = [f"{role.mention}" for role in roles]

        embed = Embed(title="Removed roles", colour=Colour.red())

        fields = [
            ("Members:", comma.join(tNames), False),
            ("Roles:", comma.join(tNames2), False),
        ]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.reply(embed=embed)

    @role.command(
        name="-create", aliases=["-c"], brief="Creates a role for the server."
    )
    @has_permissions(manage_roles=True)
    async def create_role_command(self, ctx, *, name: str):
        await ctx.guild.create_role(name=name)

        embed = Embed(title="Role created!", description=name, colour=Colour.green())

        await ctx.send(embed=embed)

    @role.command(
        name="-delete", aliases=["-d"], brief="Delete a role from the server."
    )
    @has_permissions(manage_roles=True)
    async def delete_role_command(self, ctx, roles: Greedy[Role]):
        for role in roles:
            await role.delete()

        comma = ", "
        tNames = [f"{role.name}" for role in roles]
        embed = Embed(
            title="Roles deleted", description=comma.join(tNames), colour=Colour.red()
        )

        await ctx.reply(embed=embed)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("mod")


def setup(bot):
    bot.add_cog(Mod(bot))
