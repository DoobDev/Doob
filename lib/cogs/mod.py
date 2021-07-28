from datetime import datetime, timedelta
import json
from typing import Optional
from random import randint
from discord.channel import VoiceChannel
from discord.utils import get


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

from discord_slash import cog_ext, ComponentContext
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import (
    create_button,
    create_select,
    create_actionrow,
    create_select_option,
    wait_for_component,
)

with open("config.json") as config_file:
    config = json.load(config_file)


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
            await ctx.reply("<:Dexclaimneg:869815364828160070> One or more required arguments are missing.")

        else:
            target_list = []
            for target in targets:
                if (
                    ctx.guild.me.top_role.position != target.top_role.position
                    and ctx.author.top_role.position > target.top_role.position
                ):

                    await target.kick(reason=reason)
                    target_list.append(target.display_name)
            
                else:
                    await ctx.reply(
                        "<:DAccessDenied:869815358758985779> Something went wrong.\nYou might not be able to kick that member."
                    )
            target_list_real = "\n<:Dspace:869830848743092247> <:DRightTrans:869842970415890432> ".join(target_list)
            await ctx.send(embed=Embed(
                description=f"<:Dcheckpos:869815364278702080> **Kicked:**\n<:Dspace:869830848743092247> <:DRightTrans:869842970415890432> {target_list_real}", 
                colour=ctx.author.colour
            ))

    async def mute_members(self, message, targets, reason):
        mute_role = db.field(
            "SELECT MutedRole FROM guilds WHERE GuildID = ?", message.guild.id
        )
        comma = "\n<:Dspace:869830848743092247> <:DRightTrans:869842970415890432> "
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

        embed = Embed(description=f"<:Dcheckpos:869815364278702080> **Muted:**\n<:Dspace:869830848743092247> <:DRightTrans:869842970415890432> {comma.join(tNames)}", colour=message.author.colour)
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
            await ctx.reply("<:Dexclaimneg:869815364828160070> One or more required arguments are missing.")

        else:
            unmutes = await self.mute_members(ctx.message, targets, reason)

            if len(unmutes):
                mute_role = db.field(
                    "SELECT MutedRole FROM guilds WHERE GuildID = ?", ctx.guild.id
                )
                TheRole = ctx.guild.get_role(int(mute_role))
                target_list = []
                for target in targets:
                    await target.remove_roles(TheRole)
                    db.execute(
                        f"DELETE FROM mutes WHERE UserID = {target.id} AND GuildID = {ctx.guild.id}"
                    )
                    db.commit()

                    target_list.append(target.display_name)

                target_list_real = "\n<:Dspace:869830848743092247> <:DRightTrans:869842970415890432> ".join(target_list)
                await ctx.send(embed=Embed(
                    description=f"<:Dcheckpos:869815364278702080> **Unmuted:**\n<:Dspace:869830848743092247> <:DRightTrans:869842970415890432> {target_list_real}", 
                    colour=ctx.author.colour
                ))

    @command(name="unmute", aliases=["um"], brief="Unmutes a member from the server.")
    @bot_has_permissions(manage_roles=True)
    @has_permissions(manage_roles=True)
    async def delmute_command(self, ctx, targets: Greedy[Member]):
        """Unmutes a member from the server\nRequires the `Manage Roles` permission"""
        target_list = []
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
            target_list.append(target.display_name)

        target_list_real = "\n<:Dspace:869830848743092247> <:DRightTrans:869842970415890432> ".join(target_list)
        await ctx.send(embed=Embed(
            description=f"<:Dcheckpos:869815364278702080> **Unmuted:**\n<:Dspace:869830848743092247> <:DRightTrans:869842970415890432> {target_list_real}", 
            colour=ctx.author.colour
        ))

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
            await ctx.reply(
                "<:DAccessDenied:869815358758985779> One or more required arguments are missing."
            )

        else:
            target_list = []
            for target in targets:
                if (
                    ctx.guild.me.top_role.position != target.top_role.position
                    and ctx.author.top_role.position > target.top_role.position
                ):

                    await target.ban(reason=reason)
                    target_list.append(target.display_name)
                else:
                    await ctx.reply(
                        "<:DAccessDenied:869815358758985779> Something went wrong.\n<:Dcrossneg:869815364383572059> You might not be able to ban that member."
                    )

            target_list_real = "\n<:Dspace:869830848743092247> <:DRightTrans:869842970415890432> ".join(target_list)
            
            await ctx.send(embed=Embed(
                description=f"<:Dcheckpos:869815364278702080> **Banned:**\n<:Dspace:869830848743092247> <:DRightTrans:869842970415890432> {target_list_real}", 
                colour=ctx.author.colour
            ))

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
                                "<:DAccessDenied:869815358758985779> Something went wrong.\nYou might not be able to ban that member.\nYou survived this one..."
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
            target_list = []
            for target in targets:
                await ctx.guild.unban(target, reason=reason)
                target_list.append(target.display_name)
            
            target_list_real = "\n<:Dspace:869830848743092247> <:DRightTrans:869842970415890432> ".join(target_list)
            await ctx.send(embed=Embed(
                description=f"<:Dcheckpos:869815364278702080> **Unbanned:**\n<:Dspace:869830848743092247> <:DRightTrans:869842970415890432> {target_list_real}",
                colour=ctx.author.colour
            ))


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

                await ctx.send(f"<:Dtrashcan:869815365323079733> Deleted {len(deleted):,} messages.", delete_after=10)

        else:
            await ctx.reply("<:Dexclaimneg:869815364828160070> The limit provided is not within acceptable bounds.")

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
            await ctx.reply(f"<:Dwrenchpink:869830850605375489> Log channel set to <#{channel.id}>")

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
            await ctx.reply(f"<:Dwrenchpink:869830850605375489> Starboard channel set to <#{channel.id}>")

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
            await ctx.reply(f"<:Dwrenchpink:869830850605375489> Mute role set to `{role}`")

        else:
            await ctx.reply(
                f"<:DAccessDenied:869815358758985779> Please try a different role.\nYou may need to move the `Doob` role in your server settings above the `{role}` role."
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

        await ctx.send(f"<:Dcheckpos:869815364278702080> Your Text Channel has been created.\n<#{channel.id}>")

    @command(
        name="deletetextchannel",
        aliases=["dtc", "deletetc"],
        brief="Delete a text channel.",
    )
    @has_permissions(manage_channels=True)
    async def delete_text_channel_command(self, ctx, channel: TextChannel):
        channel = self.bot.get_channel(channel.id)

        await channel.delete()

        await ctx.send(
            f"<:Dtrashcan:869815365323079733> Your Text Channel ({channel.name}: `{channel.id}`) has been deleted."
        )

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

        await ctx.send(f"<:Dcheckpos:869815364278702080> Your Voice Channel has been created.\n{invite}")

    @command(
        name="deletevoicechannel",
        aliases=["dvc", "deletevoice", "deletevc"],
        brief="Delete a voice channel.",
    )
    @has_permissions(manage_channels=True)
    async def delete_voice_channel_command(self, ctx, channel: VoiceChannel):
        channel = self.bot.get_channel(channel.id)

        await channel.delete()

        await ctx.send(
            f"<:Dtrashcan:869815365323079733> The voice channel ({channel.name}: `{channel.id}`) has been deleted."
        )

    @command(name="warn", aliases=["w"], brief="Warn a user.")
    @has_permissions(manage_guild=True)
    async def warn_command(
        self, ctx, targets: Greedy[Member], *, reason: Optional[str]
    ):
        target_list = []
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
                    f"<:Dwarning:869830849061879859> You have been warned in {ctx.guild.name} for no reason."
                )

            else:
                await user.send(
                    f"<:Dwarning:869830849061879859> You have been warned in {ctx.guild.name} for {reason}"
                )

            target_list.append(target.display_name)

        target_list_real = "\n<:Dspace:869830848743092247> <:DRightTrans:869842970415890432> ".join(target_list)
        await ctx.send(embed=Embed(
            description=f"<:Dwarningpos:869815366715584513> **Warned:**\n<:Dspace:869830848743092247> <:DRightTrans:869842970415890432> {target_list_real}",
            colour=ctx.author.colour
        ))

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
            title=f"<:Dwarning:869830849061879859> Warnings for {ctx.author.display_name}", colour=ctx.author.colour
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

    @command(name="config", brief="Configure your Doob settings.")
    async def config_command(self, ctx):
        if ctx.author.guild_permissions.manage_guild:
            embed = Embed(
                title="Doob Config",
                description="Which would you like to configure?",
                colour=ctx.author.colour,
            )

            buttons = [
                create_button(
                    style=ButtonStyle.blurple,
                    label="Server Settings",
                    custom_id="server_settings",
                ),
                create_button(
                    style=ButtonStyle.blurple,
                    label="Profile Settings",
                    custom_id="profile_settings_cmd",
                ),
            ]

            action_row = create_actionrow(*buttons)

            await ctx.send(embed=embed, components=[action_row])

        else:
            await self.profile_settings(ctx, component=False)

    @cog_ext.cog_component()
    async def server_settings(self, ctx: ComponentContext):
        prefix, log_channel, muted_role, starboard_channel, level_messages = db.record(
            "SELECT Prefix, LogChannel, MutedRole, StarBoardChannel, LevelMessages FROM guilds WHERE GuildID = ?",
            ctx.guild.id,
        )

        embed = Embed(title="Server Settings", colour=ctx.author.colour)

        level_messages = "Enabled" if level_messages == "yes" else "Disabled"

        fields = [
            ("Prefix:", f"`{prefix}` | {prefix}prefix", False),
            ("Log Channel:", f"<#{log_channel}> | {prefix}setlogchannel", False),
            ("Muted Role:", f"<@{muted_role}> | {prefix}setmuterole", False),
            (
                "Starboard Channel:",
                f"<#{starboard_channel}> | {prefix}setstarboardchannel",
                False,
            ),
            ("Level Messages:", f"`{level_messages}` | {prefix}levelmessages", False),
        ]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        buttons = [
            create_button(
                style=ButtonStyle.blurple,
                label="Server Settings",
                custom_id="server_settings",
            ),
            create_button(
                style=ButtonStyle.blurple,
                label="Profile Settings",
                custom_id="profile_settings_cmd",
            ),
        ]

        action_row = create_actionrow(*buttons)

        await ctx.edit_origin(embed=embed, components=[action_row])

    @cog_ext.cog_component()
    async def profile_settings_cmd(self, ctx: ComponentContext):
        await self.profile_settings(ctx, component=True)

    async def profile_settings(self, ctx, component: bool):
        (
            OWUsername,
            OWPlatform,
            OWRegion,
            LastfmUsername,
            osuUsername,
            ShortLinkAmount,
        ) = db.record(
            "SELECT OverwatchUsername, OverwatchPlatform, OverwatchRegion, LastfmUsername, osuUsername, ShortLinkAmount FROM users WHERE UserID = ?",
            ctx.author.id,
        )

        prefix = db.field("SELECT Prefix FROM guilds WHERE GuildID = ?", ctx.guild.id)

        embed = Embed(title="Profile Settings", colour=ctx.author.colour)

        homeGuild = self.bot.get_guild(config["homeGuild_id"])  # Support Server ID.
        patreonRole = get(
            homeGuild.roles, id=config["patreonRole_id"]
        )  # Patreon role ID.

        member = []

        # Checks if user is a Patron
        for pledger in homeGuild.members:
            if pledger == ctx.author:
                member = pledger

        if ctx.author in homeGuild.members and patreonRole in member.roles:
            ShortLinkTotal = "12"
        else:
            ShortLinkTotal = "6"

        fields = [
            ("Overwatch Username:", f"`{OWUsername}` | {prefix}setowusername", False),
            ("Overwatch Platform:", f"`{OWPlatform}` | {prefix}setowusername", False),
            ("Overwatch Region:", f"`{OWRegion}` | {prefix}setowusername", False),
            ("Last.fm Username:", f"`{LastfmUsername}` | {prefix}setlastfm", False),
            (
                "Short Link (doob.link) Amount:",
                f"`{ShortLinkAmount}/{ShortLinkTotal}` | {prefix}help links",
                False,
            ),
        ]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        if component:
            buttons = [
                create_button(
                    style=ButtonStyle.blurple,
                    label="Server Settings",
                    custom_id="server_settings",
                ),
                create_button(
                    style=ButtonStyle.blurple,
                    label="Profile Settings",
                    custom_id="profile_settings_cmd",
                ),
            ]

            action_row = create_actionrow(*buttons)

            await ctx.edit_origin(embed=embed, components=[action_row])

        else:
            await ctx.send(embed=embed)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("mod")


def setup(bot):
    bot.add_cog(Mod(bot))
