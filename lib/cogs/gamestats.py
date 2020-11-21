from discord.ext.commands import Cog, command, BucketType, cooldown

from discord import Member, Embed

from typing import Optional
from aiohttp import request

from ..db import db # pylint: disable=relative-beyond-top-level

import os
from dotenv import load_dotenv
load_dotenv()

class gamestats(Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(name="owstats", aliases=["overwatch", "owprofile", "ow"], brief="Gets your Overwatch stats.")
	@cooldown(1, 5, BucketType.user)
	async def overwatch_stats(self, ctx, target: Optional[Member]):
		"""Gets your Overwatch stats from ow-api.com!\nSet your overwatch profile by doing `doob/setowprofile {platform} {username} {region}`"""
		target = target or ctx.author

		# Grabs the platform, username, and region from the database in which the user set before running the command.
		platform =  db.record("SELECT OverwatchPlatform FROM exp WHERE UserID = ?", target.id)
		platformUserIdentifier = db.record("SELECT OverwatchUsername FROM exp WHERE UserID = ?", target.id)
		platformRegion = db.record("SELECT OverwatchRegion FROM exp WHERE UserID = ?", target.id)

		# URL of the stats API.
		URL = f"https://ow-api.com/v1/stats/{platform[0]}/{platformRegion[0]}/{platformUserIdentifier[0]}/complete"

		async with request("GET", URL) as response:
			if response.status == 200:

				data = (await response.json())['competitiveStats']['careerStats']['allHeroes']

				embed = Embed(title=f"{target.display_name}'s Overwatch Stats!", description="Competitive Stats", colour=ctx.author.colour)
				# All of the stats from the API, all into the fields.
				fields = [("Below are per 10 min average stats.", "-----------------------------------------", False),
						  ("Eliminations", f"{data['average']['eliminationsAvgPer10Min']}", True),
						  ("All Damage Done", f"{data['average']['allDamageDoneAvgPer10Min']}", True),
						  ("Final Blows", f"{data['average']['finalBlowsAvgPer10Min']}", True),
						  ("Solo Kills", f"{data['average']['soloKillsAvgPer10Min']}", True),
						  ("Time spent on fire", f"{data['average']['timeSpentOnFireAvgPer10Min']}", True),
						  ("Healing done", f"{data['average']['healingDoneAvgPer10Min']}", True),
						  ("Deaths", f"{data['average']['deathsAvgPer10Min']}", True),
						  ("Hero Damage Done", f"{data['average']['heroDamageDoneAvgPer10Min']}", True),
						  ("Below are 'best' stats", "-------------------------", False),
						  ("Eliminations", f"{data['best']['eliminationsMostInGame']}", True),
						  ("All Damage Done", f"{data['best']['allDamageDoneMostInGame']}", True),
						  ("Final Blows", f"{data['best']['finalBlowsMostInGame']}", True),
						  ("Solo Kills", f"{data['best']['soloKillsMostInGame']}", True),
						  ("Time spent on fire", f"{data['best']['timeSpentOnFireMostInGame']}", True),
						  ("Healing done", f"{data['best']['healingDoneMostInGame']}", True),
						  ("Hero Damage Done", f"{data['best']['heroDamageDoneMostInGame']}", True)]

				# Adds the fields.
				for name, value, inline in fields:
					embed.add_field(name=name, value=value, inline=inline)

				embed.set_footer(text="Sourced from ow-api.com", icon_url=ctx.author.avatar_url)
				embed.set_thumbnail(url=(await response.json())['icon'])
				await ctx.send(embed=embed)
			
			else: # If the API status is not 200, then send out this.
				await ctx.send(f"Overwatch stats [ow-api.com] API sent a {response.status} status.")

	@command(name="setowusername", aliases=["setplatform", "sowp", "sowu", "setusername"], brief="Sets your Overwatch username+platform.")
	@cooldown(1, 5, BucketType.user)
	async def set_overwatch_profile(self, ctx, platform: Optional[str], username: Optional[str], region: Optional[str]):
		"""Sets your Overwatch platform + username for `doob/owstats`\nOnly acceptable platforms are `pc` `xbl` and `psn`\nOnly acceptable regions are `us` `eu` or `asia`\nFor battletags, make sure you do `{username}-{numbers}` NOT `{username}#{numbers}`"""

		# If the platform they chose was PSN, set their Username, Platform, and Region to what they said when they executed the command
		if platform == "psn":
			embed=Embed(title="Setting Overwatch Profile:", description=f"PSN", colour=ctx.author.colour)

			embed.add_field(name="Overwatch Username", value=username)
			embed.set_thumbnail(url=ctx.author.avatar_url)

			db.execute("UPDATE exp SET OverwatchUsername = ? WHERE UserID = ?", username, ctx.author.id)
			db.execute("UPDATE exp SET OverwatchPlatform = ? WHERE UserID = ?", platform, ctx.author.id)
			db.execute("UPDATE exp SET OverwatchRegion = ? WHERE UserID = ?", region, ctx.author.id)
			db.commit()

			await ctx.send(embed=embed)

		# Same here, but with PC
		elif platform == "pc":
			embed=Embed(title="Setting Overwatch Profile:", description=f"Battle.net", colour=ctx.author.colour)

			embed.add_field(name="Overwatch Username", value=username)
			embed.set_thumbnail(url=ctx.author.avatar_url)

			db.execute("UPDATE exp SET OverwatchUsername = ? WHERE UserID = ?", username, ctx.author.id)
			db.execute("UPDATE exp SET OverwatchPlatform = ? WHERE UserID = ?", platform, ctx.author.id)
			db.execute("UPDATE exp SET OverwatchRegion = ? WHERE UserID = ?", region, ctx.author.id)
			db.commit()

			await ctx.send(embed=embed)

		# Same here, but with Xbox Live
		elif platform == "xbl":
			embed=Embed(title="Setting Overwatch Profile:", description=f"Xbox Live", colour=ctx.author.colour)

			embed.add_field(name="Overwatch Username", value=username)
			embed.set_thumbnail(url=ctx.author.avatar_url)

			db.execute("UPDATE exp SET OverwatchUsername = ? WHERE UserID = ?", username, ctx.author.id)
			db.execute("UPDATE exp SET OverwatchPlatform = ? WHERE UserID = ?", platform, ctx.author.id)
			db.execute("UPDATE exp SET OverwatchRegion = ? WHERE UserID = ?", region, ctx.author.id)
			db.commit()

			await ctx.send(embed=embed)
		
		# If they didn't want to set anything, show them what they currently have in the database.
		else:
			platform =  db.record("SELECT OverwatchPlatform FROM exp WHERE UserID = ?", ctx.author.id)
			username =  db.record("SELECT OverwatchUsername FROM exp WHERE UserID = ?", ctx.author.id)
			region = db.record("SELECT OverwatchRegion FROM exp WHERE UserID = ?", ctx.author.id)
			embed=Embed(title="Your Overwatch Profile", colour=ctx.author.colour)

			embed.add_field(name="Overwatch Username", value=username[0])
			embed.add_field(name="Overwatch Platform", value=platform[0])
			embed.add_field(name="Overwatch Region", value=region[0])
			embed.set_thumbnail(url=ctx.author.avatar_url)

			await ctx.send(embed=embed)

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("gamestats")

def setup(bot):
	bot.add_cog(gamestats(bot))