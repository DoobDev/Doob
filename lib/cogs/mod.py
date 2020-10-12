from asyncio import sleep
from datetime import datetime, timedelta
from re import search
from typing import Optional

from discord import Embed, Member, Role, TextChannel
from discord.ext.commands import Cog, Greedy
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions, bot_has_permissions

from ..db import db # pylint: disable=relative-beyond-top-level

class Mod(Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(name="kick", aliases=["k", "kickmember"], brief="Kick a member from the server.")
	@bot_has_permissions(kick_members=True)
	@has_permissions(kick_members=True)
	async def kick_command(self, ctx, targets: Greedy[Member], *, reason: Optional[str] = "No reason provided."):
		"""Kicks a member from the server. | `Kick Members` permission required."""
		if not len(targets):
			await ctx.send("One or more required arguments are missing.")

		else:
			for target in targets:
				if (ctx.guild.me.top_role.position != target.top_role.position
					and ctx.author.top_role.position > target.top_role.position):
					
					await target.kick(reason=reason)
					await ctx.send("Member Kicked.")
				else:
					await ctx.send("Something went wrong.\nYou might not be able to kick that member.")

	@kick_command.error
	async def kick_command_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			await ctx.send("Insufficient permissions to perform that task.")

# 	async def mute_members(self, message, targets, reason):
# 		unmutes = []
# 		mute_role = db.field('SELECT MutedRole FROM guilds WHERE GuildID = ?', message.guild.id)
# 		for target in targets:
# 			if not mute_role in target.roles:
        
# 				if message.guild.me.top_role.position > target.top_role.position:
# 					role_ids = ",".join([str(r.id) for r in target.roles])
# 					theRole = message.guild.get_role(int(mute_role))
# 					await target.add_roles(theRole)
# 					print("checkpoint 1")
# 					db.execute("INSERT INTO mutes VALUES (?, ?, ?)",
# 							   target.id, role_ids, message.guild.id)
# 					print("checkpoint 2")
# 					does this work?/?!?!?!?/1/11//!/1/1/1 yep it just wasn't awaited big bad :(((
# 					await message.channel.send(f"{target} has been muted (pog)")
# 					print("checkpoint 3")
# 					IT WORKED IT WORKED IT WORKED I REPEAT IT WORKEDkmn
# 					time to work on unmute Sadge its ez its legit just remove role it shouldnt have taken us this long for an add role command

# 					This is why raw SQL sucks, matt.
# 					no :)
# 					we are doing indefinente mutes anyway, we dont need an end time column
# 					i deleted the db OMEGTALUL
# 					i know
# 					ik shut up
# wait if theres no muted role set it wont work
# 					epic :sunglasses:
					
# 					db.execute("INSERT INTO mutes VALUES (?, ?, ?)",
# 							   target.id, role_ids, getattr(end_time, "isoformat", lambda: None)())
					
					
			

# 					embed = Embed(title="Member muted",
# 								  colour=0xDD2222,
# 								  timestamp=datetime.utcnow())

# 					embed.set_thumbnail(url=target.avatar_url)

# 					fields = [("Member", target.display_name, False),
# 							  ("Actioned by", message.author.display_name, False),
# 							  ("Reason", reason, False)]

# 					for name, value, inline in fields:
# 						embed.add_field(name=name, value=value, inline=inline)
# 					log_channel = message.guild.get_channel(db.field("SELECT LogChannel FROM guilds WHERE GuildID  = ?", message.guild.id))

# 					#It needs to be the role object.
                    
# 					await log_channel.send(embed=embed)

# 					if hours:
# 						unmutes.append(target)
# 		return unmutes

# 	@command(name="mute")
# 	@has_permissions(ban_members=True)
# 	@bot_has_permissions(manage_roles=True)
# 	@has_permissions(manage_roles=True, manage_guild=True)
# 	async def mute_command(self, ctx, targets: Greedy[Member], *,
# 						   reason: Optional[str] = "No reason provided."):
# 		if not len(targets):
# 			await ctx.send("One or more required arguments are missing.")

# 		else:
# 			unmutes = await self.mute_members(ctx.message, targets, reason)
# 			await ctx.send("Action complete.")

# 			if len(unmutes):
# 				mute_role = db.field('SELECT MutedRole FROM guilds WHERE GuildID = ?', ctx.guild.id) 
# 				TheRole = ctx.guild.get_role(int(mute_role))
# 				for target in targets:
# 					await target.remove_roles(TheRole)
# 					db.execute("DELETE FROM mutes WHERE VALUES = (?, ?)", target.id, ctx.guild.id)
# 					await ctx.send("Unmuted! <:PogU:560267624966258690>")

# 	@command(name="unmute")
# 	@has_permissions(ban_members=True)
# 	@bot_has_permissions(manage_roles=True)
# 	@has_permissions(manage_roles=True, manage_guild=True)
# 	async def delmute_command(self, ctx, targets: Greedy[Member]):
# 		mute_role = db.field('SELECT MutedRole FROM guilds WHERE GuildID = ?', ctx.guild.id) 
# 		TheRole = ctx.guild.get_role(int(mute_role))
# 		for target in targets:
# 			await target.remove_roles(TheRole)
# 			db.execute("DELETE FROM mutes WHERE VALUES = (?, ?)", target.id, ctx.guild.id)
# 			await ctx.send("Unmuted! <:PogU:560267624966258690>")
# lmfao xD easy way out 
# idk raw sql so u do this :)
# i think i did it right lol
#        do the other one... :|
#oooooooooooooooooooooooooooooooooooooohkewl :thumsup:
# EZbut we need to get my completion message working 
# yeah it didn't work before sooooo! lmfao
# 	@mute_command.error
# 	async def mute_command_error(self, ctx, exc):
# 		if isinstance(exc, CheckFailure):
# 			await ctx.send("Insufficient permissions to perform that task.")

	@command(name="ban", aliases=["b", "banmember"], brief="Ban a member from the server.")
	@bot_has_permissions(ban_members=True)
	@has_permissions(ban_members=True)
	async def ban_command(self, ctx, targets: Greedy[Member], *, reason: Optional[str] = "No reason provided."):
		"""Bans a member from the server | `Ban Members` permission required."""
		if not len(targets):
			await ctx.send("One or more required arguments are missing.")

		else:
			for target in targets:
				if (ctx.guild.me.top_role.position != target.top_role.position
					and ctx.author.top_role.position > target.top_role.position):
					
					await target.ban(reason=reason)
					await ctx.send("Member banned.")
				
				else: 
					await ctx.send("Something went wrong.\nYou might not be able to ban that member.")
	@ban_command.error
	async def ban_command_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			await ctx.send("Insufficient permissions to perform that task.")

	@command(name="clear", aliases=["purge"], brief="Clears amount of messages provided.")
	@bot_has_permissions(manage_messages=True)
	@has_permissions(manage_messages=True)
	async def clear_messages(self, ctx, targets: Greedy[Member], limit: Optional[int] = 1):
		"""Clears an ammount of messages provided by the user. | `Manage Messages` permission required."""
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
	async def set_log_channel(self, ctx, *, channel: Optional[TextChannel]):
		"""Sets the logging channel for the server. | `Manage Server` permission required."""
		prefix = db.records("SELECT Prefix FROM guilds WHERE GuildID = ?", ctx.guild.id)
		if channel == None:
			await ctx.send(f"The current setting for the Log Channel is: `{channel}`\nTo change it, type `{str(prefix)}setlogchannel #<log channel>`")

		else:
			db.execute("UPDATE guilds SET LogChannel = ? WHERE GuildID = ?", str(channel.id), ctx.guild.id)
			db.commit()
			await ctx.send(f"Log channel set to <#{channel.id}>")

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("mod")
		
	@command(name="setmuterole", aliases=["smr", "muterole", "setmute"], brief="Set the server's mute role.")
	@has_permissions(manage_guild=True)
	async def set_mute_role(self, ctx, *, role: Optional[Role]):
		"""Sets the `Muted` role for your server. | `Manage Server` premission required."""
		prefix = db.records("SELECT Prefix FROM guilds WHERE GuildID = ?", ctx.guild.id)
		if role == None:
			await ctx.send(f"The current setting for the Muted role is: `{role}`\nTo change it, type `{str(prefix)}setmuterole @<muted role>`")

		elif ctx.guild.me.top_role.position > role.position:
			db.execute("UPDATE guilds SET MutedRole = ? WHERE GuildID = ?", str(role.id), ctx.guild.id)
			db.commit()
			await ctx.send(f"Mute role set to `{role}`")

		else:
			await ctx.send(f"Please try a different role.\nYou may need to move the `Doob` role in your server settings above the `{role}` role.")

def setup(bot):
	bot.add_cog(Mod(bot))