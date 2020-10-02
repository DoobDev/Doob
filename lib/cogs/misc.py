from discord.ext.commands import Cog
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions, cooldown, BucketType
from discord import Embed

from ..db import db # pylint: disable=relative-beyond-top-level

class Misc(Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(name="prefix", aliases=["ChangePrefix"], brief="Changes the prefix.")
	@has_permissions(manage_guild=True)
	async def change_prefix(self, ctx, new: str):
		"""Changes the prefix for the server. | `Manage Server` permission required."""
		if len(new) > 10:
			await ctx.send("The prefix can not be more than 10 characters.", delete_after=10)

		else:
			db.execute("UPDATE guilds SET Prefix = ? WHERE GuildID = ?", new, ctx.guild.id)
			embed = Embed(title="Prefix Changed", description=f"Prefix has been changed to `{new}`")
			await ctx.send(embed=embed)

	@change_prefix.error
	async def change_prefix_error(self, ctx, exc):
		if isinstance(exc, CheckFailure):
			await ctx.send("You need the Manage Server permission to change the prefix.", delete_after=10)

	@command(name="poll", brief="Lets the user create a poll.")
	@cooldown(1, 4, BucketType.user)
	async def start_poll(self, ctx, *, question: str):
		"""Starts a poll with the question/name the user wants!"""
		embed = Embed(title="Poll Started", description=question, colour=ctx.author.colour)
		embed.set_footer(text=f"{ctx.author} started this poll.", icon_url=ctx.author.avatar_url)
		message = await ctx.send(embed=embed)

		emojis = ['✅', '❌']

		for emoji in emojis:
			await message.add_reaction(emoji)

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("misc")

def setup(bot):
	bot.add_cog(Misc(bot))