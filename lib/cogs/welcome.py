from discord import Forbidden
from discord.ext.commands import Cog
from discord.ext.commands import command

from ..db import db # pylint: disable=relative-beyond-top-level

class Welcome(Cog):
	def __init__(self, bot):
		self.bot = bot

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("welcome")

	@Cog.listener()
	async def on_member_join(self, member):
		db.execute("INSERT INTO exp (UserID) VALUES (?)", member.id)

	@Cog.listener()
	async def on_member_remove(self, member):
		db.execute("DELETE FROM exp WHERE UserID = ?", member.id)

	@Cog.listener()
	async def on_guild_join(self, guild):
		db.execute("INSERT INTO guilds WHERE GuildID = ?", guild.id)

def setup(bot):
	bot.add_cog(Welcome(bot))