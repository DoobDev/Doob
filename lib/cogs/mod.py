from asyncio import sleep
from typing import Optional
from datetime import datetime, timedelta


from discord import Member, Embed, Role
from discord.ext.commands import Cog, CheckFailure, command, has_permissions, bot_has_permissions, Greedy

from ..db import db # pylint: disable=relative-beyond-top-level

class Mod(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="kick", aliases=["k"], brief="Kicks a member.")
    @bot_has_permissions(kick_members=True)
    @has_permissions(kick_members=True)
    async def kick_members(self, ctx, targets: Greedy[Member], *, reason: Optional[str] = "No reason."):
        if not len(targets):
            await ctx.message.delete()
            await ctx.send("Required arguments missing", delete_after=10)

        else:
            for target in targets:
                if ctx.guild.me.top_role.position > target.top_role.position:
                    await target.kick(reason=reason)
                    # embed=Embed(title="User has been Kicked", description=f"{target.name} has been kicked from the server", timestamp=datetime.utcnow())
                    # embed.add_field(name="Reason", value=reason)
                    # embed.set_thumbnail(url=target.avatar_url)
                    # embed.set_footer(text=f"Kicked by {ctx.author.name}", icon_url=ctx.author.avatar_url)
                    #await self.log_channel.seld(embed=embed)
                else:
                    await ctx.message.delete()
                    await ctx.send(f"{target.display_name} could not be banned.", delete_after=10)
            await ctx.send(f"{target.name} has been kicked {reason}")

    @kick_members.error
    async def kick_members_errors(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.message.delete()
            await ctx.send("Don't have permission to kick members.", delete_after=10)

    @command(name="ban", aliases=["b"], brief="Bans a member.")
    @bot_has_permissions(ban_members=True)
    @has_permissions(ban_members=True)
    async def ban_members(self, ctx, targets: Greedy[Member], *, reason: Optional[str] = "No reason."):
        if not len(targets):
            await ctx.message.delete()
            await ctx.send("Required arguments missing", delete_after=10)

        else:
            for target in targets:
                if ctx.guild.me.top_role.position > target.top_role.position:
                    await target.ban(reason=reason)
                    # embed=Embed(title="User has been Banned", description=f"{target.name} has been banned from the server", timestamp=datetime.utcnow())
                    # embed.add_field(name="Reason", value=reason)
                    # embed.set_thumbnail(url=target.avatar_url)
                    # embed.set_footer(text=f"Banned by {ctx.author.name}", icon_url=ctx.author.avatar_url)
                    #await self.log_channel.seld(embed=embed)
                else:
                    await ctx.message.delete()
                    await ctx.send(f"{target.display_name} could not be banned.", delete_after=10)
            await ctx.send(f"{target.name} has been banned {reason}")

    @ban_members.error
    async def ban_members_errors(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.message.delete()
            await ctx.send("Don't have permission to ban members.", delete_after=10)

    @command(name="clear", aliases=["purge", "p", "c"], brief="Clears messages")
    @bot_has_permissions(manage_messages=True)
    @has_permissions(manage_messages=True)
    async def clear_messages(self, ctx, limit: Optional[int] = 1):
        if 0 < limit <= 100:
            with ctx.channel.typing():
                await ctx.message.delete()
                await ctx.channel.purge(limit=limit)
                
                await ctx.send(f"Cleared {limit} messages.", delete_after=10)
        else:
            await ctx.message.delete()
            await ctx.send("Amount of cleared messages provided were was either too big or too small.")

    # @command(name="mute", aliases=["m"], brief="Mutes member.")
    # @bot_has_permissions(manage_roles=True)
    # @has_permissions(manage_roles=True, manage_guild=True)
    # async def mute_members(self, ctx, targets: Greedy[Member], minutes: Optional[int] , *, reason: Optional[str] = "No reason."):
    #     if not len(targets):
    #         await ctx.send("Required arguments missing")

    #     else:
    #         unmutes = []

    #         for target in targets:
    #             if not self.mute_role in target.roles:
    #                 if ctx.guild.me.top_role.position > target.top_role.position:
    #                     role_ids = ",".join([str(r.id) for r in target.roles])
    #                     end_time = datetime.utcnow() + timedelta(seconds=minutes*60) if minutes else None

    #                     db.execute("INSERT INTO mutes VALUES (?, ?, ?)", target.id, role_ids, getattr(end_time, "isoformat", lambda: None)())

    #                     await target.edit(roles=[self.mute_role])
                    
    #                 # embed=Embed(title="User has been Muted", description=f"{target.name} has been muted", timestamp=datetime.utcnow())
    #                 # embed.add_field(name="Reason", value=reason)
    #                 # embed.add_field(name="Duration", value = f"{minutes:,} minute(s) if minutes else "Indefinite")
    #                 # embed.set_thumbnail(url=target.avatar_url)
    #                 # embed.set_footer(text=f"Muted by {ctx.author.name}", icon_url=ctx.author.avatar_url)
    #                 #await self.log_channel.seld(embed=embed)

    #                 if minutes:
    #                     unmutes.append(target)

    #             else:
    #                 await ctx.send(f"{target.name} could not be muted")
    #         else:
    #             await ctx.send(f"{target.name} is already muted.")

    #     await ctx.send(f"{target.name} muted for {minutes} minutes.")

    #     if len(unmutes):
    #         await sleep(minutes)
    #         await self.unmute(ctx, targets)

    # @mute_members.error
    # async def mute_members_error(self, ctx, exc):
    #     if isinstance(exc, CheckFailure):
    #         await ctx.send("Don't have permission to mute members.")

    # async def unmute(self, ctx, targets, *, reason="Mute time expired."):
    #     for target in targets:
    #         if self.mute_role in target.roles:
    #             role_ids = db.field("SELECT RoleIDs FROM mutes WHERE UserID = ?", target.id)
    #             roles = [ctx.guild.get_role(int(id_)) for id_ in role_ids.split(",") if len(id_)]

    #             db.execute("DELETE FROM mutes WHERE UserID = ?", target.id)

    #             await target.edit(roles=roles)

    #                 # embed=Embed(title="User has been unmuted", description=f"{target.name} has been unmuted", timestamp=datetime.utcnow())
    #                 # embed.add_field(name="Reason", value=reason)
    #                 # embed.set_thumbnail(url=target.avatar_url)
    #                 #await self.log_channel.seld(embed=embed)

    # @command(name="unmute", aliases=["um"], brief="Unmutes a member")
    # @bot_has_permissions(manage_roles=True)
    # @has_permissions(manage_roles=True, manage_guild=True)
    # async def unmute_members(self, ctx, targets: Greedy[Member], *, reason: Optional[str] = "No reason."):
    #     if not len(targets):
    #         await ctx.send("Required arguments missing.")

    #     else:
    #         await self.unmute(ctx, targets, reason=reason)\

    # @command(name="SetMuteRole", aliases=["smr"])
    # @has_permissions(manage_guild=True)
    # async def set_mute_role(self, ctx, target: Role):
    #     if not len(target):
    #         await ctx.send("Required arguments missing.")

    #     else:
    #         db.execute("INSERT INTO guilds (MutedRole) VALUES (?)", target)
    #         await ctx.send(f"Set the Muted Role as {target}")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            #self.log_channel = bot.get_logchannel(GET FROM DB, MATT DO THIS LATER)
            #self.mute_role = self.bot.guild_getrole(GET FROM DB, MATT DO THIS LATER)
            self.bot.cogs_ready.ready_up("mod")

def setup(bot):
    bot.add_cog(Mod(bot))