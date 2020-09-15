from discord.ext.commands import Cog
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions

from ..db import db # pylint: disable=relative-beyond-top-level

class Misc(Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(name="prefix", aliases=["ChangePrefix"], brief="Changes the prefix.")
	@has_permissions(manage_guild=True)
	async def change_prefix(self, ctx, new: str):
		if len(new) > 10:
			await ctx.message.delete()
			await ctx.send("The prefix can not be more than 10 characters.", delete_after=10)

		else:
			db.execute("UPDATE guilds SET Prefix = ? WHERE GuildID = ?", new, ctx.guild.id)
			await ctx.send(f"Prefix set to {new}")

	@change_prefix.error
	async def change_prefix_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			await ctx.message.delete()
			await ctx.send("You need the Manage Server permission to change the prefix.", delete_after=10)

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("misc")

def setup(bot):
	bot.add_cog(Misc(bot))