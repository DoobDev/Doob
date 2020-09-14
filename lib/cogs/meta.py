from platform import python_version
from time import time
from datetime import datetime, timedelta

from apscheduler.triggers.cron import CronTrigger
from discord import Activity, ActivityType, Embed
from discord import __version__ as discord_version
from discord.ext.commands import Cog
from discord.ext.commands import command, BucketType, cooldown, is_owner

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

    @command(name="setactivity", brief="Set the bot's activity")
    async def set_activity_message(self, ctx, *, text: str):
        if ctx.author.id == owner_id:
            self.message = text
            await self.set()
            await ctx.send(f"Bot Status has been updated to {text}")
        else:
            await ctx.send("You don't have permission to do that.")

    @command(name="ping", brief="Shows the bot's latency.")
    @cooldown(1, 10, BucketType.user)
    async def ping(self, ctx):
        start = time()
        message = await ctx.send("Loading...")
        end = time()
        await message.edit(content=f"Pong! :ping_pong: Latency: {self.bot.latency*1000:,.0f} ms. Response time: {(end-start)*1000:,.0f} ms.")

    @command(name="shutdown")
    async def shutdown(self, ctx):
        if ctx.author.id == owner_id:
            await ctx.send("Shutting down")

            db.commit()
            self.bot.scheduler.shutdown()
            await self.bot.logout()
        else:
            await ctx.send("You don't have permission to shutdown the bot.")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("meta")

def setup(bot):
    bot.add_cog(Meta(bot))