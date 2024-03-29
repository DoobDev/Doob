import io
import logging
from time import time
from datetime import datetime, timedelta
from typing import Optional
import discord
import textwrap
from discord.ext import commands
from traceback import format_exception
from psutil import Process, virtual_memory
from platform import python_version
from apscheduler.triggers.cron import CronTrigger
from discord.ext.buttons import Paginator
import contextlib
from asyncio import sleep
from pathlib import Path

from discord import Activity, ActivityType, Embed, Member
from discord import __version__ as discord_version

from discord.ext.commands import Cog, command, BucketType, cooldown, Greedy

from discord.utils import get

from discord_slash.utils.manage_commands import create_option
from discord_slash import cog_ext, SlashContext

from ..db import db  # pylint: disable=relative-beyond-top-level

import os

log = logging.getLogger()

cwd = Path(__file__).parents[0]
cwd = str(cwd)

import json

with open("config.json") as config_file:
    config = json.load(config_file)

owner_id = config["owner_ids"][0]


class Meta(Cog):
    def __init__(self, bot):
        self.bot = bot

        self.message = "playing @Doob help | {users:,} members in {guilds:,} servers. Version - {VERSION}"

        bot.scheduler.add_job(self.set, CronTrigger(second=0))

    @property
    def message(self):
        return self._message.format(
            users=len(self.bot.users),
            guilds=len(self.bot.guilds),
            VERSION=self.bot.VERSION,
        )

    @message.setter
    def message(self, value):
        if value.split(" ")[0] not in ("playing", "watching", "listening", "streaming"):
            raise ValueError("Invalid activity.")

        self._message = value

    async def set(self):
        _type, _name = self.message.split(" ", maxsplit=1)
        await self.bot.change_presence(
            activity=Activity(
                name=_name, type=getattr(ActivityType, _type, ActivityType.playing)
            )
        )

    @command(name="setactivity", brief="Owner Only Command - Set the bot's activity")
    @commands.is_owner()
    async def set_activity_message(self, ctx, *, text: str):
        """Set the bot's `playing` or `watching`, etc status.\n`Owner` permission required."""
        self.message = text
        await self.set()
        await ctx.reply(f"Bot Status has been updated to {text}")

    @command(
        name="support",
        aliases=["supportserver"],
        brief="Get a link to the Doob support server.",
    )
    async def support_server_link(self, ctx):
        """Gives a link to the Doob Support Server where you can get help from the developer!"""
        await ctx.reply("Join the support server at: :link: https://discord.gg/hgQTTU7")

    @cog_ext.cog_slash(
        name="support", description="Get a link to the Doob support server."
    )
    async def support_server_link_slashcmd(self, ctx):
        await ctx.send("Join the support server at: :link: https://discord.gg/hgQTTU7")

    @command(
        name="invite",
        aliases=["invitebot", "inv", "botinvite"],
        brief="Gives a link to invite Doob to your server.",
    )
    async def doob_invite_link(self, ctx):
        """Gives you a link to invite Doob to another server!"""
        await ctx.reply(
            "You can invite the bot here! :link: <https://doob.link/invite>"
        )

    @cog_ext.cog_slash(
        name="invite", description="Gives a link to invite Doob to your server."
    )
    async def doob_invite_link_slashcmd(self, ctx):
        await ctx.send("You can invite the bot here! :link: <https://doob.link/invite>")

    @command(name="ping", brief="Shows the bot's latency.")
    @cooldown(1, 10, BucketType.user)
    async def ping(self, ctx):
        """Ping Pong!~\nShows the bot latency and response time."""
        start = time()
        message = await ctx.reply("Loading... <a:loadingdoob:755141175840866364>")
        end = time()
        await message.edit(
            content=f"Pong! :ping_pong: Latency: {self.bot.latency*1000:,.0f} ms. Response time: {(end-start)*1000:,.0f} ms."
        )

    @command(
        name="shutdown", brief="Owner Only Command to shutdown the bot and save the DB."
    )
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Command to shutdown the bot and save it's database.\n`Owner` permission required"""
        await ctx.reply("Shutting down")

        db.commit()
        self.bot.scheduler.shutdown()
        await self.bot.logout()

    @command(name="restart", brief="Owner Only Command to restart the bot.")
    @commands.is_owner()
    async def restart(self, ctx):
        """Command to restart, and update the bot to its latest version.\n`Owner` permission required"""
        await ctx.reply("Restarting...")

        db.commit()
        self.bot.scheduler.shutdown()
        await self.bot.logout()

        log.info("Fetching latest version from doobdev/doob@master")
        os.system("git pull origin master")
        log.info("Installing requirements.txt")
        os.system("python3.9 -m pip install -r requirements.txt  --force-reinstall")
        log.info("Starting bot.")
        os.system("python3.9 launcher.py")

    @command(
        name="update", brief="Owner Only Command to give a pretty embed for updates."
    )
    @commands.is_owner()
    async def update_command(self, ctx, *, update: str):
        """Command to give people updates on why bot was going down / brief patch notes\n`Owner` permission required"""

        prefix = db.records("SELECT Prefix from guilds WHERE GuildID = ?", ctx.guild.id)

        with ctx.channel.typing():
            await ctx.message.delete()
            embed = Embed(title="Update:", description=update, colour=ctx.author.colour)
            embed.set_author(
                name=f"All the patch notes for {self.bot.VERSION} available here.",
                url=f"https://github.com/doobdev/doob/blob/master/CHANGELOG.md#v{self.bot.VERSION.replace('.', '')}",
            )
            embed.set_footer(
                text=f"Authored by: {ctx.author.display_name}",
                icon_url=ctx.author.avatar_url,
            )
            await ctx.send(embed=embed)

    async def show_bot_info(self, ctx, patreon_status):
        embed = Embed(
            title="Doob Info  <:doob:754762131085459498>",
            colour=ctx.author.colour,
            timestamp=datetime.utcnow(),
        )

        bot_version = self.bot.VERSION

        proc = Process()
        with proc.oneshot():
            uptime = timedelta(seconds=time() - proc.create_time())
            cpu_time = timedelta(
                seconds=(cpu := proc.cpu_times()).system + cpu.user
            )  # pylint: disable=used-before-assignment
            mem_total = virtual_memory().total / (1025 ** 2)
            mem_of_total = proc.memory_percent()
            mem_usg = mem_total * (mem_of_total / 100)

        fields = [
            ("Name", "Doob <:doob:754762131085459498>", False),
            (
                "Description",
                "The multipurpose Discord Bot with global leveling and powerful logging tools for your server.",
                False,
            ),
            ("Developers", "<@308000668181069824>", False),
            ("Doob's Server Count", f"{str(len(self.bot.guilds))}", True),
            ("Doob's Member Count", f"{str(len(self.bot.users))}", True),
            (
                "The ping for Doob is...",
                f" :ping_pong: {round(self.bot.latency * 1000)} ms",
                False,
            ),
            ("Python Version", python_version(), True),
            ("Uptime", uptime, True),
            ("CPU Time", cpu_time, True),
            (
                "Memory Usage",
                f"{mem_usg:,.3f} MiB / {mem_total:,.0f} MiB ({mem_of_total:.0f}%)",
                True,
            ),
            ("Library", f"discord.py {discord_version}", True),
            (
                "Bot Version",
                f"{self.bot.VERSION} - [Changelog](https://github.com/doobdev/doob/blob/master/CHANGELOG.md#v{bot_version.replace('.', '')})",
                True,
            ),
            ("Top.gg Link", "https://top.gg/bot/680606346952966177", False),
            (
                "Invite Link",
                "[Invite Link Here](https://doob.link/invite)",
                True,
            ),
            (
                "GitHub Repository",
                "[Click Here](https://github.com/doobdev/doob)",
                True,
            ),
        ]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        embed.set_thumbnail(url=ctx.guild.me.avatar_url)
        embed.set_footer(
            text=f"{ctx.author.name} requested Doob's information",
            icon_url=ctx.author.avatar_url,
        )

        if patreon_status == True:
            embed.add_field(
                name="Patreon",
                value=f"Thanks for [Donating](https://patreon.com/doobdev) {ctx.author.display_name}! :white_check_mark:",
                inline=False,
            )
            await ctx.reply(embed=embed)

        if patreon_status == False:
            embed.add_field(
                name="Patreon",
                value="[Click Here for Patreon](https://patreon.com/doobdev)",
                inline=False,
            )
            await ctx.reply(embed=embed)

    @command(name="info", aliases=["botinfo"], brief="Gives basic info about Doob.")
    async def show_bot_info_command(self, ctx):
        """Gives basic info about Doob."""

        homeGuild = self.bot.get_guild(config["homeGuild_id"])  # Support Server ID.
        patreonRole = get(
            homeGuild.roles, id=config["patreonRole_id"]
        )  # Patreon role ID.

        member = []

        for pledger in homeGuild.members:
            if pledger == ctx.author:
                member = pledger

        if ctx.author in homeGuild.members and patreonRole in member.roles:
            await self.show_bot_info(ctx, patreon_status=True)

        else:
            await self.show_bot_info(ctx, patreon_status=False)

    @command(
        name="patreon",
        aliases=["donate", "donation"],
        brief="Show support to Doob Dev!",
    )
    async def patreon_link(self, ctx):
        """Gives a link to the Patreon for Doob!\nWe apprecieate your support!~"""
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
                f"Thanks for supporting {ctx.author.mention}!\n<https://patreon.com/doobdev>"
            )

        else:
            await ctx.reply(
                "You can support Doob Dev by subscribing at <https://patreon.com/doobdev>!"
            )

    class Pag(Paginator):
        async def teardown(self):
            try:
                await self.page.clear_reactions()
            except discord.HTTPException:
                pass

    @command(name="eval", hidden=True)
    @commands.is_owner()
    async def _eval(self, ctx, *, code: str):
        def clean_code(content):
            if content.startswith("```") and content.endswith("```"):
                return "\n".join(content.split("\n")[1:])[:-3]
            else:
                return content

        code = clean_code(code)

        local_variables = {
            "discord": discord,
            "commands": commands,
            "bot": self.bot,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "self": self,
        }

        stdout = io.StringIO()

        try:
            with contextlib.redirect_stdout(stdout):
                exec(
                    f"async def func():\n{textwrap.indent(code, '    ')}",
                    local_variables,
                )

                obj = await local_variables["func"]()
                result = f"{stdout.getvalue()}\n-- {obj}\n"

        except Exception as e:
            result = "".join(format_exception(e, e, e.__traceback__))

        pager = self.Pag(
            timeout=100,
            entries=[result[i : i + 2000] for i in range(0, len(result), 2000)],
            length=1,
            prefix="```py\n",
            suffix="```",
        )

        await pager.start(ctx)

    @command(name="blacklist", brief="Adds a user to the Doob blacklist.")
    @commands.is_owner()
    async def blacklist_user(
        self, ctx, users: Greedy[Member], *, reason: Optional[str]
    ):
        data = self.read_json("blacklisted_users")

        for user in users:
            if user.id not in data["blacklist"]:
                db.execute(
                    "INSERT OR IGNORE INTO blacklist (UserID, Reason) VALUES (?, ?)",
                    user.id,
                    reason,
                )
                db.commit()

                data["blacklist"].append(user.id)
                self.write_json(data, "blacklisted_users")
                await ctx.send(f"{user.name} has been blacklisted for {reason}.")
                await user.send(
                    f"❌You have been blacklisted from using Doob for {reason}"
                )
            else:
                await ctx.send(f"{user.name} is already blacklisted.")

    @command(name="unblacklist", brief="Removes a user from the Doob blacklist.")
    @commands.is_owner()
    async def unblacklist_user(self, ctx, users: Greedy[Member]):
        data = self.read_json("blacklisted_users")

        for user in users:
            if user.id in data["blacklist"]:
                db.execute("DELETE FROM blacklist WHERE UserID = ?", user.id)
                db.commit()

                data["blacklist"].remove(user.id)
                self.write_json(data, "blacklisted_users")

                await ctx.send(f"{user.name} has been unblacklisted.")
                await user.send(f"✅You have been unblacklisted from using Doob.")
            else:
                await ctx.send(f"{user.name} is not blacklisted.")

    def read_json(self, filename):
        with open(f"{cwd}/{filename}.json", "r") as file:
            data = json.load(file)
        return data

    def write_json(self, data, filename):
        with open(f"{cwd}/{filename}.json", "w") as file:
            json.dump(data, file, indent=4)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("meta")


def setup(bot):
    bot.add_cog(Meta(bot))
