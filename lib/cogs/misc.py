from discord.ext.commands import Cog
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions, cooldown, BucketType
from discord import Embed, Message, Reaction

import requests

import json

import random

from ..db import db # pylint: disable=relative-beyond-top-level

owner_id = 308000668181069824

import os
from dotenv import load_dotenv
load_dotenv()

class Misc(Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(name="prefix", aliases=["ChangePrefix"], brief="Changes the prefix.")
	@has_permissions(manage_guild=True)
	async def change_prefix(self, ctx, new: str):
		"""Changes the prefix for the server.\n`Manage Server` permission required."""
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

	
	@command(name="giveaway", aliases=['startgiveaway'], brief="Creates a giveaway, that will choose a winner!")
	@cooldown(1, 5, BucketType.user)
	@has_permissions(administrator=True)
	async def start_giveaway(self, ctx, *, prize: str):
		"""Lets a Server Admin start a giveaway\n`Server Administrator` permission required."""
		embed=Embed(title=f"{prize} giveaway!", description=f"{ctx.author.display_name} is giving away {prize}!\nReact with 🎁!")
		embed.set_footer(text=f"{ctx.author} started this giveaway.", icon_url=ctx.author.avatar_url)

		message = await ctx.send(embed=embed)

		await message.add_reaction('🎁')

	@command(name="stopgiveaway", aliases=['endgiveaway'], brief="Stops the giveaway, this chooses the winner!")
	@cooldown(1, 5, BucketType.user)
	@has_permissions(administrator=True)
	async def stop_giveaway(self, ctx, *, message_id: Message):
		"""Lets a Server Admin stop a giveaway, this chooses the winner at random!\n`Server Administrator` permission required."""

		channel = self.bot.get_channel(message_id.channel.id)
		message = await channel.fetch_message(message_id.id)

		users = set()

		for reaction in message.reactions:
			async for user in reaction.users():
				if not user.bot:
					users.add(user)

		entries = list()

		for user in users:
			if not user.bot:
				entries.append(user.id)
			else:
				print("lol")

		winner = random.choice(entries)

		print(entries)

		await channel.send(f"<@{winner}> won the giveaway!")
		await channel.send(f"{ctx.author.mention}, the giveaway has been ended.", delete_after=30)

		user = self.bot.get_user(winner)

		await user.send(f'You won the giveaway from <#{channel.id}> in {channel.guild.name}!')

	@command(name="timebomb", aliases=["tbmsg", "tb", "timebombmessage"], brief="Send a message with a timelimit on it.")
	@cooldown(1, 4, BucketType.user)
	async def time_bomb_command(self, ctx, time: int, *, message : str):
		"""Makes a message with a timelimit on it, the time is in seconds."""
		if time >= 1000:
			await ctx.message.delete()

			embed = Embed(title="Time Message", description=message, colour=ctx.author.colour)
			embed.set_thumbnail(url=ctx.author.avatar_url)
			embed.set_footer(text=f"{ctx.author} | This message only lasts {str(time)} seconds.", icon_url=ctx.author.avatar_url)

			await ctx.send(embed=embed, delete_after=time)

		else:
			await ctx.send("Please try again with a lower time.", delete_after=15)

	@command(name="vote", aliases=["upvote"], brief="Vote for Doob on Top.gg!")
	@cooldown(1, 4, BucketType.user)
	async def topgg_upvote_command(self, ctx):
		await ctx.send("Vote for Doob at: https://top.gg/bot/680606346952966177/vote")

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("misc")

def setup(bot):
	bot.add_cog(Misc(bot))