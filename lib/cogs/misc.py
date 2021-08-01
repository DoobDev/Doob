import logging
from pathlib import Path
from typing import Optional
from discord.ext import commands
from discord.ext.commands import Cog
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions, cooldown, BucketType
from discord import Embed, Message, Emoji, TextChannel

from discord_slash.utils.manage_commands import create_option
from discord_slash import cog_ext

from discord.utils import get

from datetime import datetime

import json

with open("config.json") as config_file:
    config = json.load(config_file)

import random

from ..db import db  # pylint: disable=relative-beyond-top-level

owner_id = config["owner_ids"][0]

import os
from dotenv import load_dotenv
import time as t

load_dotenv()
log = logging.getLogger()

cwd = Path(__file__).parents[0]
cwd = str(cwd)


def read_json(filename):
    with open(f"./lib/cogs/{filename}.json", "r") as file:
        data = json.load(file)
    return data


def write_json(data, filename):
    with open(f"{cwd}/{filename}.json", "w") as file:
        json.dump(data, file, indent=4)


class Misc(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="afk", aliases=["away", "brb"])
    @cooldown(1, 10, BucketType.user)
    async def afk_command(self, ctx, *, message: Optional[str] = "brb"):
        afk = read_json("afk")

        time = datetime.now()
        time_real = t.mktime(time.timetuple()) + time.microsecond / 1e6

        afk[str(ctx.author.id)] = {"message": message, "time": str(time_real)}

        write_json(afk, "afk")

        await ctx.send(f"{ctx.author.mention} is now AFK: {message}")

    @command(name="prefix", aliases=["ChangePrefix"], brief="Changes the prefix.")
    @has_permissions(manage_guild=True)
    async def change_prefix(self, ctx, new: str):
        """Changes the prefix for the server.\n`Manage Server` permission required."""
        if len(new) > 10:
            await ctx.reply(
                "The prefix can not be more than 10 characters.", delete_after=10
            )

        else:
            db.execute(
                "UPDATE guilds SET Prefix = ? WHERE GuildID = ?", new, ctx.guild.id
            )
            embed = Embed(
                title="Prefix Changed",
                description=f"Prefix has been changed to `{new}`",
            )
            await ctx.reply(embed=embed)

    @change_prefix.error
    async def change_prefix_error(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.reply(
                "You need the Manage Server permission to change the prefix.",
                delete_after=10,
            )

    @command(name="poll", brief="Lets the user create a poll.")
    @cooldown(1, 4, BucketType.user)
    async def start_poll_command(self, ctx, *, question: str):
        """Starts a poll with the question/name the user wants!"""
        embed = Embed(
            title="Poll Started!", description=question, colour=ctx.author.colour
        )
        embed.set_footer(
            text=f"{ctx.author} started this poll.", icon_url=ctx.author.avatar_url
        )
        message = await ctx.send(embed=embed)

        emojis = ["✅", "❌"]

        for emoji in emojis:
            await message.add_reaction(emoji)

    @cog_ext.cog_slash(
        name="poll",
        description="Start a poll!",
        options=[
            create_option(
                name="question",
                description="What you want to ask the users.",
                option_type=3,
                required=True,
            )
        ],
    )
    async def start_poll_slash(self, ctx, question: str):
        embed = Embed(
            title="Poll Started!", description=question, colour=ctx.author.colour
        )
        embed.set_footer(
            text=f"{ctx.author} started this poll.", icon_url=ctx.author.avatar_url
        )
        message = await ctx.send(embed=embed)

        emojis = ["✅", "❌"]

        for emoji in emojis:
            await message.add_reaction(emoji)

    @command(name="endpoll", brief="Lets a user end a poll.")
    @cooldown(1, 5, BucketType.user)
    async def end_poll_command(self, ctx, *, message_id: Message):
        """Ends the poll and shows results."""
        channel = self.bot.get_channel(message_id.channel.id)
        message = await channel.fetch_message(message_id.id)

        reaction1 = get(message.reactions, emoji="✅")
        reaction2 = get(message.reactions, emoji="❌")

        if reaction1.count > reaction2.count:
            winner = "✅"
            winner_count = reaction1.count
            loser_count = reaction2.count
        elif reaction2.count > reaction1.count:
            winner = "❌"
            winner_count = reaction2.count
            loser_count = reaction1.count

        else:
            winner = "Tie!"

        if winner == "Tie!":
            embed = Embed(
                title="Poll ended!", description="Poll ended in a tie!", colour=0xFFFF00
            )

        elif winner == "❌":
            embed = Embed(
                title="Poll ended!",
                description=f"{winner} has won by {winner_count-loser_count} votes!",
                colour=0xAE0700,
            )

        elif winner == "✅":
            embed = Embed(
                title="Poll ended!",
                description=f"{winner} has won by {winner_count-loser_count} votes!",
                colour=0x66FF00,
            )

        embed.set_footer(
            text=f"Poll ended by: {ctx.author.display_name}",
            icon_url=ctx.author.avatar_url,
        )

        await message.edit(embed=embed)

    @cog_ext.cog_slash(
        name="endpoll",
        description="End an existing poll!",
        options=[
            create_option(
                name="message_id",
                description="The poll's message ID you would like to end.",
                option_type=3,
                required=True,
            ),
            create_option(
                name="channel",
                description="Channel the poll was sent in.",
                option_type=7,
                required=True,
            ),
        ],
    )
    async def end_poll_slash(self, ctx, channel: TextChannel, message_id: str):
        channel = self.bot.get_channel(channel.id)
        message = await channel.fetch_message(message_id)

        reaction1 = get(message.reactions, emoji="✅")
        reaction2 = get(message.reactions, emoji="❌")

        if reaction1.count > reaction2.count:
            winner = "✅"
            winner_count = reaction1.count
            loser_count = reaction2.count
        elif reaction2.count > reaction1.count:
            winner = "❌"
            winner_count = reaction2.count
            loser_count = reaction1.count

        else:
            winner = "Tie!"

        if winner == "Tie!":
            embed = Embed(
                title="Poll ended!", description="Poll ended in a tie!", colour=0xFFFF00
            )

        elif winner == "❌":
            embed = Embed(
                title="Poll ended!",
                description=f"{winner} has won by {winner_count-loser_count} votes!",
                colour=0xAE0700,
            )

        elif winner == "✅":
            embed = Embed(
                title="Poll ended!",
                description=f"{winner} has won by {winner_count-loser_count} votes!",
                colour=0x66FF00,
            )

        embed.set_footer(
            text=f"Poll ended by: {ctx.author.display_name}",
            icon_url=ctx.author.avatar_url,
        )

        await message.edit(embed=embed)

        await ctx.send("Poll Completed!", hidden=True)

    @command(
        name="giveaway",
        aliases=["startgiveaway"],
        brief="Creates a giveaway, that will choose a winner!",
    )
    @cooldown(1, 5, BucketType.user)
    @has_permissions(administrator=True)
    async def start_giveaway(self, ctx, *, prize: str):
        """Lets a Server Admin start a giveaway\n`Server Administrator` permission required."""
        embed = Embed(
            title=f"{prize} giveaway!",
            description=f"{ctx.author.display_name} is giving away {prize}!\nReact with 🎁!",
        )
        embed.set_footer(
            text=f"{ctx.author} started this giveaway.", icon_url=ctx.author.avatar_url
        )

        message = await ctx.reply(embed=embed)

        await message.add_reaction("🎁")

    @command(
        name="stopgiveaway",
        aliases=["endgiveaway"],
        brief="Stops the giveaway, this chooses the winner!",
    )
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

        entries = []

        for user in users:
            if not user.bot:
                entries.append(user.id)

        winner = random.choice(entries)

        log.info(entries)

        await channel.send(f"<@{winner}> won the giveaway!")
        await channel.send(
            f"{ctx.author.mention}, the giveaway has been ended.", delete_after=30
        )

        user = self.bot.get_user(winner)

        await user.send(
            f"You won the giveaway from <#{channel.id}> in {channel.guild.name}!"
        )

    @command(
        name="timebomb",
        aliases=["tbmsg", "tb", "timebombmessage"],
        brief="Send a message with a timelimit on it.",
    )
    @cooldown(1, 4, BucketType.user)
    async def time_bomb_command(self, ctx, time: int, *, message: str):
        """Makes a message with a timelimit on it, the time is in seconds."""
        if time < 1000:
            await ctx.message.delete()

            embed = Embed(
                title="Time Message", description=message, colour=ctx.author.colour
            )
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.set_footer(
                text=f"{ctx.author} | This message only lasts {str(time)} seconds.",
                icon_url=ctx.author.avatar_url,
            )

            await ctx.send(embed=embed, delete_after=time)

        else:
            await ctx.reply(
                f"Please try again with a lower time, {time} is too big.",
                delete_after=15,
            )

    @command(name="vote", aliases=["upvote"], brief="Vote for Doob on Top.gg!")
    @cooldown(1, 4, BucketType.user)
    async def topgg_upvote_command(self, ctx):
        await ctx.reply("Vote for Doob at: https://top.gg/bot/680606346952966177/vote")

    @command(name="phone", aliases=["iphone"], brief="phone")
    @cooldown(1, 4, BucketType.user)
    async def phone_command(self, ctx):
        """phone\n`Patreon Only`"""
        homeGuild = self.bot.get_guild(config["homeGuild_id"])  # Support Server ID.
        patreonRole = get(
            homeGuild.roles, id=config["patreonRole_id"]
        )  # Patreon role ID.

        member = []

        for pledger in homeGuild.members:
            if pledger == ctx.author:
                member = pledger

        if ctx.author in homeGuild.members and patreonRole in member.roles:
            await ctx.reply(
                "https://cdn.discordapp.com/attachments/721514198000992350/794840218514751499/IYUimA7gyac7sxrB3uKu9Mb1ZZOJVtgAAAA.png"
            )

        else:
            await ctx.reply(
                "You are not a Patron to Doob, subscribe to any of the tiers at <https://patreon.com/doobdev> to gain access to this command."
            )

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("misc")

    @command(
        name="ownerprefix",
        aliases=["opo"],
        brief="Changes the prefix. | Bot Owner Override.",
    )
    @commands.is_owner()
    async def override_change_prefix(self, ctx, new: str):
        """Changes the prefix for the server.\nOnly the bot owner can use the override command."""

        prefix = db.records("SELECT Prefix FROM guilds WHERE GuildID = ?", ctx.guild.id)

        db.execute("UPDATE guilds SET Prefix = ? WHERE GuildID = ?", new, ctx.guild.id)
        embed = Embed(
            title="Prefix Changed",
            description=f"Prefix has been changed to `{new}`",
        )

        await ctx.reply(embed=embed)

    @command(
        name="overlay", aliases=["streamkit"], brief="Gives Discord Streamkit Overlay."
    )
    @cooldown(1, 5, BucketType.user)
    async def streamkit_overlay_command(self, ctx):
        """Gives a Discord Streamkit Overlay link for your Livestreams"""

        # super long URL so im just making it into a variable
        streamkit_url = f"https://streamkit.discord.com/overlay/voice/{ctx.guild.id}/{ctx.author.voice.channel.id}?icon=true&online=true&logo=white&text_color=%23ffffff&text_size=14&text_outline_color=%23000000&text_outline_size=0&text_shadow_color=%23000000&text_shadow_size=0&bg_color=%231e2124&bg_opacity=0.95&bg_shadow_color=%23000000&bg_shadow_size=0&invite_code=&limit_speaking=false&small_avatars=false&hide_names=false&fade_chat=0"

        embed = Embed(
            title="Streamkit Overlay:",
            description=streamkit_url,
            colour=ctx.author.colour,
            timestamp=datetime.utcnow(),
        )
        embed.set_footer(
            text=f"Requested By: {ctx.author}", icon_url=ctx.message.author.avatar_url
        )
        embed.set_thumbnail(
            url="https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/OBS.svg/1024px-OBS.svg.png"
        )
        await ctx.send(embed=embed)

    @streamkit_overlay_command.error
    async def streamkit_overlay_command_error(self, ctx, exc):
        if hasattr(exc, "original") and isinstance(exc.original, AttributeError):
            await ctx.message.delete()
            await ctx.send(
                "Please join a voice channel before running the `overlay` command.",
                delete_after=15,
            )

    @command(name="emote", aliases=["emoji"], brief="Gets Emote info.")
    async def get_emote_command(self, ctx, emote: Emoji):
        embed = Embed(
            title=f"{emote.name} Info",
            colour=ctx.author.colour,
            timestamp=datetime.utcnow(),
        )

        fields = [
            ("Name", emote.name, False),
            ("ID", emote.id, False),
            ("Does the emote require colons?", emote.require_colons, False),
            ("Animated?", emote.animated, False),
            ("Twitch Sub Emote?", emote.managed, False),
            ("Guild", emote.guild.name, False),
            # ("Creator", emote.user.username, False),
            ("Created At", emote.created_at, False),
            ("URL", emote.url, False),
        ]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        embed.set_image(url=emote.url)

        await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(Misc(bot))
