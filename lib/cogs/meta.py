from time import time
from datetime import datetime, timedelta
from typing import Optional

from apscheduler.triggers.cron import CronTrigger
from discord import Activity, ActivityType, Embed, Member
from discord import __version__ as discord_version
from discord.ext.commands import Cog
from discord.ext.commands import command, BucketType, cooldown
from discord.utils import get

from ..db import db # pylint: disable=relative-beyond-top-level

owner_id = 308000668181069824

class Meta(Cog):
	def __init__(self, bot):
		self.bot = bot

		self.message = "playing @Doob help | {users:,} members in {guilds:,} servers. Version - {VERSION}"

		bot.scheduler.add_job(self.set, CronTrigger(second=0))

	@property
	def message(self):
		return self._message.format(users=len(self.bot.users), guilds = len(self.bot.guilds), VERSION = self.bot.VERSION)

	@message.setter
	def message(self, value):
		if value.split(" ")[0] not in ("playing", "watching", "listening", "streaming"):
			raise ValueError("Invalid activity.")

		self._message = value

	async def set(self):
		_type, _name = self.message.split(" ", maxsplit=1)
		await self.bot.change_presence(activity=Activity(
			name=_name,
			type=getattr(ActivityType, _type, ActivityType.playing)
		))

	@command(name="setactivity", brief="Owner Only Command - Set the bot's activity")
	async def set_activity_message(self, ctx, *, text: str):
		"""Set the bot's `playing` or `watching`, etc status.\n`Owner` permission required."""
		if ctx.author.id == owner_id:
			self.message = text
			await self.set()
			await ctx.send(f"Bot Status has been updated to {text}")
		else:
			await ctx.send("You don't have permission to do that.")

	@command(name="support", aliases=["supportserver"], brief="Get a link to the Doob support server.")
	async def support_server_link(self, ctx):
		"""Gives a link to the Doob Support Server where you can get help from the developer!"""
		await ctx.send("Join the support server at: :link: https://discord.gg/hgQTTU7")

	@command(name="invite", aliases=["invitebot", "inv", "botinvite"], brief="Gives a link to invite Doob to your server.")
	async def doob_invite_link(self, ctx):
		"""Gives you a link to invite Doob to another server!"""
		await ctx.send("You can invite the bot here! :link: <https://discordapp.com/oauth2/authorize?client_id=680606346952966177&scope=bot&permissions=271674430>")

	@command(name="ping", brief="Shows the bot's latency.")
	@cooldown(1, 10, BucketType.user)
	async def ping(self, ctx):
		"""Ping Pong!~\nShows the bot latency and response time."""
		start = time()
		message = await ctx.send("Loading...")
		end = time()
		await message.edit(content=f"Pong! :ping_pong: Latency: {self.bot.latency*1000:,.0f} ms. Response time: {(end-start)*1000:,.0f} ms.")

	@command(name="shutdown", brief="Owner Only Command to shutdown the bot and save the DB.")
	async def shutdown(self, ctx):
		"""Command to shutdown the bot and save it's database.\n`Owner` permission required"""
		if ctx.author.id == owner_id:
			await ctx.send("Shutting down")

			db.commit()
			self.bot.scheduler.shutdown()
			await self.bot.logout()
		else:
			await ctx.send("You don't have permission to shutdown the bot.")

	@command(name="nitrogiveaway", brief="Owner Only Command to tell people how to enter the Nitro Giveaways for Doob.")
	async def nitro_giveaway_command(self, ctx, *, target: Optional[Member]):
		"""Command to tell people how to claim the Discord Nitro Classic gift.\n`Owner` permission required"""
		if ctx.author.id == owner_id:
			# await ctx.send(f"{target}, To claim the Discord Nitro Classic gift, check <#757666920773189662> to see if the Nitro has been claimed for this week!\nDon't know when to claim the Nitro? If you have gotten a Lucky Dog (from doing `doob/dog`) DM `mmatt#001` with a screenshot!")
			await ctx.send(f"{target.mention}, Lucky Dog Nitro Giveaways!\nGet the most lucky dogs in the month (check how many you have by doing `doob/luckydogs`) and you can win Nitro Classic!\nCheck <#757666920773189662> to see if someone has claimed it for this month!")

		else:
			await ctx.send("You don't have permission to use this command.", delete_after=10)

	@command(name="update", brief="Owner Only Command to give a pretty embed for updates.")
	async def update_command(self, ctx, *, update: str):
		"""Command to give people updates on why bot was going down / brief patch notes\n`Owner` permission required"""

		prefix = db.records("SELECT Prefix from guilds WHERE GuildID = ?", ctx.guild.id)

		if ctx.author.id == owner_id:
			with ctx.channel.typing():
				await ctx.message.delete()
				embed=Embed(title="Update:", description=update, colour=ctx.author.colour)
				embed.set_author(name=f"All the patch notes for {self.bot.VERSION} available here.", url=f"https://github.com/doobdev/doob/blob/master/CHANGELOG.md#v{self.bot.VERSION.replace('.', '')}")
				embed.set_footer(text=f"Authored by: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
				await ctx.send(embed=embed)
		elif ctx.author.id != owner_id:
			await ctx.send(f"You don't have permissions to give updates about Doob\nType `{prefix[0][0]}help update` for more info.")

	@command(name="info", aliases=["botinfo"], brief="Gives basic info about Doob.")
	async def show_basic_bot_info(self, ctx):
		"""Gives basic info about Doob."""

		homeGuild = self.bot.get_guild(702352937980133386)
		patreonRole = get(homeGuild.roles, id=757041749716893739)

		member = []

		for pledger in homeGuild.members:
			if pledger == ctx.author:
				member = pledger

		if ctx.author in homeGuild.members:
			if patreonRole in member.roles:
				embed = Embed(title="Doob Info", colour=ctx.author.colour, timestamp=datetime.utcnow())

				bot_version = self.bot.VERSION

				fields = [("Name", "Doob", False),
							("Description", "A Discord bot made by mmatt using discord.py, he felt like making it so he did B)", False),
							("Developers", "<@308000668181069824>, <@476188720521805825>", False),
							("Doob's Server Count", f"{str(len(self.bot.guilds))}", True),
							("Doob's Member Count", f"{str(len(self.bot.users))}", True),
							("The ping for Doob is...", f" :ping_pong: {round(self.bot.latency * 1000)} ms", False),
							("Library", "discord.py", True),
							("Bot Version", f"{self.bot.VERSION} - [Changelog](https://github.com/doobdev/doob/blob/master/CHANGELOG.md#v{bot_version.replace('.', '')})", True),
							("Top.gg Link", "https://top.gg/bot/680606346952966177", False),
							("Invite Link", "[Invite Link Here](https://discordapp.com/oauth2/authorize?client_id=680606346952966177&scope=bot&permissions=271674430)", True),
							("GitHub Repository", "[Click Here](https://github.com/doobdev/doob)", True),
							("Patreon", f"Thanks for [Donating](https://patreon.com/doobdev) {ctx.author}! :white_check_mark:", False)]

				for name, value, inline in fields:
					embed.add_field(name=name, value=value, inline=inline)

				embed.set_thumbnail(url=ctx.guild.me.avatar_url)
				embed.set_footer(text=f"{ctx.author.name} requested Doob's information", icon_url=ctx.author.avatar_url)

				await ctx.send(embed=embed)
			else:
				embed = Embed(title="Doob Info", colour=ctx.author.colour, timestamp=datetime.utcnow())

				bot_version = self.bot.VERSION

				fields = [("Name", "Doob", False),
							("Description", "A Discord bot made by mmatt using discord.py, he felt like making it so he did B)", False),
							("Developers", "<@308000668181069824>, <@476188720521805825>", False),
							("Doob's Server Count", f"{str(len(self.bot.guilds))}", True),
							("Doob's Member Count", f"{str(len(self.bot.users))}", True),
							("The ping for Doob is...", f" :ping_pong: {round(self.bot.latency * 1000)} ms", False),
							("Library", "discord.py", True),
							("Bot Version", f"{self.bot.VERSION} - [Changelog](https://github.com/doobdev/doob/blob/master/CHANGELOG.md#v{bot_version.replace('.', '')})", True),
							("Top.gg Link", "https://top.gg/bot/680606346952966177", False),
							("Invite Link", "[Invite Link Here](https://discordapp.com/oauth2/authorize?client_id=680606346952966177&scope=bot&permissions=271674430)", True),
							("GitHub Repository", "[Click Here](https://github.com/doobdev/doob)", True),
							("Patreon", "[Donate to Doob and get cool perks!](https://patreon.com/doobdev)", False)]

				for name, value, inline in fields:
					embed.add_field(name=name, value=value, inline=inline)

				embed.set_thumbnail(url=ctx.guild.me.avatar_url)
				embed.set_footer(text=f"{ctx.author.name} requested Doob's information", icon_url=ctx.author.avatar_url)

				await ctx.send(embed=embed)

		else:
			embed = Embed(title="Doob Info", colour=ctx.author.colour, timestamp=datetime.utcnow())

			bot_version = self.bot.VERSION

			fields = [("Name", "Doob", False),
						("Description", "A Discord bot made by mmatt using discord.py, he felt like making it so he did B)", False),
						("Developers", "<@308000668181069824>, <@476188720521805825>", False),
						("Doob's Server Count", f"{str(len(self.bot.guilds))}", True),
						("Doob's Member Count", f"{str(len(self.bot.users))}", True),
						("The ping for Doob is...", f" :ping_pong: {round(self.bot.latency * 1000)} ms", False),
						("Library", "discord.py", True),
						("Bot Version", f"{self.bot.VERSION} - [Changelog](https://github.com/doobdev/doob/blob/master/CHANGELOG.md#v{bot_version.replace('.', '')})", True),
						("Top.gg Link", "https://top.gg/bot/680606346952966177", False),
						("Invite Link", "[Invite Link Here](https://discordapp.com/oauth2/authorize?client_id=680606346952966177&scope=bot&permissions=271674430)", True),
						("GitHub Repository", "[Click Here](https://github.com/doobdev/doob)", True),
						("Patreon", "[Donate to Doob and get cool perks!](https://patreon.com/doobdev)", False)]

			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)

			embed.set_thumbnail(url=ctx.guild.me.avatar_url)
			embed.set_footer(text=f"{ctx.author.name} requested Doob's information", icon_url=ctx.author.avatar_url)

			await ctx.send(embed=embed)

	@command(name="patreon", aliases=["donate", "donation"], brief="Show support to Doob Dev!")
	async def patreon_link(self, ctx):
		"""Gives a link to the Patreon for Doob!\nWe apprecieate your support!~"""
		homeGuild = self.bot.get_guild(702352937980133386)
		patreonRole = get(homeGuild.roles, id=757041749716893739)

		member = []

		for pledger in homeGuild.members:
			if pledger == ctx.author:
				member = pledger

		if ctx.author in homeGuild.members:
			if patreonRole in member.roles:
				await ctx.send(f"Thanks for supporting {ctx.author.mention}!\n<https://patreon.com/doobdev>") 

			else:
				await ctx.send("You can support Doob Dev by subscribing at <https://patreon.com/doobdev>!")

		else:
			await ctx.send("You can support Doob Dev by subscribing at <https://patreon.com/doobdev>!")

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("meta")

def setup(bot):
	bot.add_cog(Meta(bot))
