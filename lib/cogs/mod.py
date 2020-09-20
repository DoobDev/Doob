from asyncio import sleep
from datetime import datetime, timedelta
from re import search
from typing import Optional

from discord import Embed, Member
from discord.ext.commands import Cog, Greedy
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions, bot_has_permissions

from ..db import db # pylint: disable=relative-beyond-top-level

class Mod(Cog):
	def __init__(self, bot):
		self.bot = bot

	async def kick_members(self, message, targets, reason):
		for target in targets:
			if (message.guild.me.top_role.position > target.top_role.position 
				and not target.guild_permissions.administrator):
				await target.kick(reason=reason)

				embed = Embed(title="Member kicked",
							  colour=0xDD2222,
							  timestamp=datetime.utcnow())

				embed.set_thumbnail(url=target.avatar_url)

				fields = [("Member", f"{target.name} a.k.a. {target.display_name}", False),
						  ("Actioned by", message.author.display_name, False),
						  ("Reason", reason, False)]

				for name, value, inline in fields:
					embed.add_field(name=name, value=value, inline=inline)

				logchannel = self.bot.fetch_channel(db.field("SELECT LogChannel FROM guilds WHERE GuildID = ?", message.guild.id))
				await logchannel.send(embed=embed)

	@command(name="kick", aliases=["k", "kickmember"], brief="Kick a member from the server.")
	@bot_has_permissions(kick_members=True)
	@has_permissions(kick_members=True)
	async def kick_command(self, ctx, targets: Greedy[Member], *, reason: Optional[str] = "No reason provided."):
		if not len(targets):
			await ctx.send("One or more required arguments are missing.")

		else:
			await self.kick_members(ctx.message, targets, reason)
			await ctx.send("Action complete.")

	@kick_command.error
	async def kick_command_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			await ctx.send("Insufficient permissions to perform that task.")

	async def ban_members(self, message, targets, reason):
		for target in targets:
			if (message.guild.me.top_role.position > target.top_role.position 
				and not target.guild_permissions.administrator):
				await target.ban(reason=reason)

				embed = Embed(title="Member banned",
							  colour=0xDD2222,
							  timestamp=datetime.utcnow())

				embed.set_thumbnail(url=target.avatar_url)

				fields = [("Member", f"{target.name} a.k.a. {target.display_name}", False),
						  ("Actioned by", message.author.display_name, False),
						  ("Reason", reason, False)]

				for name, value, inline in fields:
					embed.add_field(name=name, value=value, inline=inline)

				logchannel = self.bot.fetch_channel(db.field("SELECT LogChannel FROM guilds WHERE GuildID = ?", message.guild.id))
				await logchannel.send(embed=embed)

  async def mute_members(self, message, targets, minutes, reason):	
    unmutes = []	
    mute_role = message.guild.get_role(db.field("SELECT MutedRole FROM guilds WHERE GuildID = ?", message.guild.id))	
    for target in targets:	
      if not mute_role in target.roles:	
        if message.guild.me.top_role.position > target.top_role.position:	
          role_ids = ",".join([str(r.id) for r in target.roles])	
          end_time = datetime.utcnow() + timedelta(seconds=minutes * 60) if minutes else None	

          db.execute("INSERT INTO mutes VALUES (?, ?, ?)",	
                  target.id, role_ids, getattr(end_time, "isoformat", lambda: None)())	

          db.commit()	

          await target.edit(roles=[mute_role])	

          embed = Embed(title="Member muted",	
                  colour=0xDD2222,	
                  timestamp=datetime.utcnow())	

          embed.set_thumbnail(url=target.avatar_url)	

          fields = [("Member", target.display_name, False),	
                ("Actioned by", message.author.display_name, False),	
                ("Duration", f"{minutes:,} hour(s)" if minutes else "Indefinite", False),	
                ("Reason", reason, False)]	

          for name, value, inline in fields:	
            embed.add_field(name=name, value=value, inline=inline)	

          logchannel = self.bot.fetch_channel(db.field("SELECT LogChannel FROM guilds WHERE GuildID = ?", message.guild.id))	
          await logchannel.send(embed=embed)	

          if minutes:	
            unmutes.append(target)	

    return unmutes	

	@command(name="mute")	
	@bot_has_permissions(manage_roles=True)	
	@has_permissions(manage_roles=True, manage_guild=True)	
	async def mute_command(self, ctx, targets: Greedy[Member], minutes: Optional[int], *,	
						   reason: Optional[str] = "No reason provided."):	
		if not len(targets):	
			await ctx.send("One or more required arguments are missing.")	

		else:	
			unmutes = await self.mute_members(ctx.message, targets, minutes, reason)	
			await ctx.send("Action complete.")	

			if len(unmutes):	
				await sleep(minutes)	
				await self.unmute_members(ctx.guild, targets)	

	@mute_command.error	
	async def mute_command_error(self, ctx, exc):	
		if isinstance(exc, CheckFailure):	
			await ctx.send("Insufficient permissions to perform that task.")	
"""
unmute deaf thingy 

defum
"""
	async def unmute_members(self, message, targets, *, reason="Mute time expired."):	
		mute_role = message.get_role(db.field("SELECT MutedRole FROM guilds WHERE GuildID = ?", message.guild.id))	
		for target in targets:
			if mute_role in target.roles:	
				role_ids = db.field("SELECT RoleIDs FROM mutes WHERE UserID = ?", target.id)	
				roles = [message.get_role(int(id_)) for id_ in role_ids.split(",") if len(id_)]	

				db.execute("DELETE FROM mutes WHERE UserID = ?", target.id)	

				db.commit()	

				await target.edit(roles=roles)	

				embed = Embed(title="Member unmuted",	
							  colour=0xDD2222,	
							  timestamp=datetime.utcnow())	


				embed.set_thumbnail(url=target.avatar_url)

				fields = [("Member", target.display_name, False),	
						  ("Reason", reason, False)]	

				for name, value, inline in fields:	
					embed.add_field(name=name, value=value, inline=inline)	


"""
actual unmute cmd for find in page search thingy

keywords:
um
unmute
umcmd
eee
"""
	@command(name="unmute")	
	@bot_has_permissions(manage_roles=True)	
	@has_permissions(manage_roles=True, manage_guild=True)	
	async def unmute_command(self, ctx, targets: Greedy[Member], *, reason: Optional[str] = "No reason provided."):	
		if not len(targets):	
			await ctx.send("One or more required arguments are missing.")	

		else:	
			await self.unmute_members(ctx.guild, targets, reason=reason)

	@command(name="ban", aliases=["b", "banmember"], brief="Ban a member from the server.")
	@bot_has_permissions(ban_members=True)
	@has_permissions(ban_members=True)
	async def ban_command(self, ctx, targets: Greedy[Member], *, reason: Optional[str] = "No reason provided."):
		if not len(targets):
			await ctx.send("One or more required arguments are missing.")

		else:
			await self.ban_members(ctx.message, targets, reason)
			await ctx.send("Action complete.")

	@ban_command.error
	async def ban_command_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			await ctx.send("Insufficient permissions to perform that task.")

	@command(name="clear", aliases=["purge"], brief="Clears amount of messages provided.")
	@bot_has_permissions(manage_messages=True)
	@has_permissions(manage_messages=True)
	async def clear_messages(self, ctx, targets: Greedy[Member], limit: Optional[int] = 1):
		def _check(message):
			return not len(targets) or message.author in targets

		if 0 < limit <= 100:
			with ctx.channel.typing():
				await ctx.message.delete()
				deleted = await ctx.channel.purge(limit=limit, after=datetime.utcnow()-timedelta(days=14),
												  check=_check)

				await ctx.send(f"Deleted {len(deleted):,} messages.", delete_after=5)

		else:
			await ctx.send("The limit provided is not within acceptable bounds.")

	@command(name="setlogchannel", aliases=["slc", "logchannel", "setlog", "setlogs"], brief="Set the server's log channel.")
	@has_permissions(manage_guild=True)
	async def set_log_channel(self, ctx, *, channel_id: str):
		if not len(channel_id):
			await ctx.send("One or more required areguments are missing.")

		else:
			db.execute("UPDATE guilds SET LogChannel = ? WHERE GuildID = ?", channel_id, ctx.guild.id)
			db.commit()
			await ctx.send(f"Log channel set to {channel_id}")

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("mod")
		
	@command(name="setmuterole", aliases=["smr", "muterole", "setmute"], brief="Set the server's mute role.")
	@has_permissions(manage_guild=True)
	async def set_mute_role(self, ctx, *, role_id: str):
		if not len(role_id):
			await ctx.send("One or more required areguments are missing.")

		else:
			db.execute("UPDATE guilds SET MutedRole = ? WHERE GuildID = ?", role_id, ctx.guild.id)
			db.commit()
			await ctx.send(f"Mute role set to {role_id}")

def setup(bot):
	bot.add_cog(Mod(bot))