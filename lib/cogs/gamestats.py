from discord.ext.commands import Cog
from discord.ext.commands import command, BucketType, cooldown

from discord import Member, Embed

from typing import Optional
from aiohttp import request

from ..db import db # pylint: disable=relative-beyond-top-level

class gamestats(Cog):
	def __init__(self, bot):
		self.bot = bot
		with open("./lib/bot/trackergg api.txt", "r", encoding="utf-8") as apikey:
			self.token = apikey.read()

	@command(name="owstats", aliases=["overwatch", "owprofile", "ow"], brief="Gets your Overwatch stats.")
	@cooldown(1, 5, BucketType.user)
	async def overwatch_stats(self, ctx, target: Optional[Member]):
		"""Gets your Overwatch stats from tracker.gg!\nSet your overwatch profile by doing `doob/setowprofile {platform} {username}`"""
		target = target or ctx.author
		platform =  db.record("SELECT OverwatchPlatform FROM exp WHERE UserID = ?", target.id)
		platformUserIdentifier = db.record("SELECT OverwatchUsername FROM exp WHERE UserID = ?", target.id)
		URL = f"https://public-api.tracker.gg/v2/overwatch/standard/profile/{platform}/{platformUserIdentifier}"

		async with request("GET", URL, headers={'TRN-Api-Key': self.token}) as response:
			if response.status == 200:
				data = await response.json()
				embed = Embed(title=f"{ctx.author}'s Overwatch Stats!", description="Sourced from [Tracker.gg](https://tracker.gg)", colour=ctx.author.colour)
				
				fields = ["got em", data["things"], False]

				for name, value, inline in fields:
					embed.add_field(name=name, value=value, inline=inline)

				embed.set_footer(text=f"{ctx.author} requested this fact!", icon_url=ctx.author.avatar_url)
				await ctx.send(embed=embed)
			else:
				print(await response.json())
				await ctx.send(f"Overwatch stats [Tracker.gg] API sent a {response.status} status.")

	@command(name="setowprofile", aliases=["setow", "owset", "setoverwatch"], brief="Sets your Overwatch profile.")
	@cooldown(1, 10, BucketType.user)
	async def set_overwatch_profile(self, ctx, platform: Optional[str], *, username: Optional[str]):
		"""Sets your Overwatch platform + profile for `doob/owstats`\nOnly acceptable platforms are `battlenet` `xbl` and `psn`"""

		if platform == "psn":
			embed=Embed(title="Setting Overwatch Profile:", description=f"PSN", colour=ctx.author.colour)

			embed.add_field(name="Overwatch Username", value=username)
			embed.set_thumbnail(url=ctx.author.avatar_url)

			db.execute("UPDATE exp SET OverwatchUsername = ? WHERE UserID = ?", username, ctx.author.id)
			db.execute("UPDATE exp SET OverwatchPlatform = ? WHERE UserID = ?", platform, ctx.author.id)
			db.commit()

			await ctx.send(embed=embed)

		elif platform == "battlenet":
			embed=Embed(title="Setting Overwatch Profile:", description=f"Battle.net", colour=ctx.author.colour)

			embed.add_field(name="Overwatch Username", value=username)
			embed.set_thumbnail(url=ctx.author.avatar_url)

			db.execute("UPDATE exp SET OverwatchUsername = ? WHERE UserID = ?", username, ctx.author.id)
			db.execute("UPDATE exp SET OverwatchPlatform = ? WHERE UserID = ?", platform, ctx.author.id)
			db.commit()

			await ctx.send(embed=embed)

		elif platform == "xbl":
			embed=Embed(title="Setting Overwatch Profile:", description=f"Xbox Live", colour=ctx.author.colour)

			embed.add_field(name="Overwatch Username", value=username)
			embed.set_thumbnail(url=ctx.author.avatar_url)

			db.execute("UPDATE exp SET OverwatchUsername = ? WHERE UserID = ?", username, ctx.author.id)
			db.execute("UPDATE exp SET OverwatchPlatform = ? WHERE UserID = ?", platform, ctx.author.id)
			db.commit()

			await ctx.send(embed=embed)
		
		else:
			platform =  db.record("SELECT OverwatchPlatform FROM exp WHERE UserID = ?", ctx.author.id)
			username =  db.record("SELECT OverwatchUsername FROM exp WHERE UserID = ?", ctx.author.id)
			embed=Embed(title="Your Overwatch Profile", colour=ctx.author.colour)

			embed.add_field(name="Overwatch Username", value=username)
			embed.add_field(name="Overwatch Platform", value=platform)
			embed.set_thumbnail(url=ctx.author.avatar_url)

			await ctx.send(embed=embed)

	@command(name="csgostats", aliases=["csgo", "csstats", "cstats", "csgoprofile", "cs"])
	@cooldown(1, 5, BucketType.user)
	async def csgo_stats(self, ctx, target: Optional[Member]):
		"""Gets your CSGO stats from tracker.gg!\nSet your CSGO profile by doing `doob/setcsgoprofile {username}`"""
		target = target or ctx.author
		platformUserIdentifier =  db.record("SELECT CSGOUsername FROM exp WHERE UserID = ?", target.id)
		URL = f"https://public-api.tracker.gg/v2/csgo/standard/profile/steam/{platformUserIdentifier}"

		async with request("GET", URL, headers={'TRN-Api-Key': self.token}) as response:
			if response.status == 200:
				data = await response.json()
				embed = Embed(title=f"{ctx.author}'s CSGO Stats!", description="Sourced from [Tracker.gg](https://tracker.gg)", colour=ctx.author.colour)
				
				fields = ["Time Played", 'GAMING', False]

				print(data["data"]["segments"]["timePlayed"]["displayValue"])

				for name, value, inline in fields:
					embed.add_field(name=name, value=value, inline=inline)

				embed.set_footer(text=f"{ctx.author} requested this fact!", icon_url=ctx.author.avatar_url)
				await ctx.send(embed=embed)
			else:
				print(await response.json())
				await ctx.send(f"CSGO stats [Tracker.gg] API sent a {response.status} status.")

	@command(name="setcsgoprofile", aliases=["setcs", "csset", "setcsgo"], brief="Sets your CSGO profile.")
	@cooldown(1, 5, BucketType.user)
	async def set_csgo_profile(self, ctx, *, username: Optional[str]):
		"""Sets your CSGO username for `doob/csgostats`"""
		embed=Embed(title="Setting CSGO Profile:", description=f"{ctx.author}", colour=ctx.author.colour)

		embed.add_field(name="Steam Username", value=username)
		embed.set_thumbnail(url=ctx.author.avatar_url)

		db.execute("UPDATE exp SET CSGOUsername = ? WHERE UserID = ?", username, ctx.author.id)
		db.commit()

		await ctx.send(embed=embed)

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("gamestats")

def setup(bot):
	bot.add_cog(gamestats(bot))