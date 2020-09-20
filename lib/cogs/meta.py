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
	
	@command(name="support", aliases=["supportserver"], brief="Get a link to the Doob support server.")
	async def support_server_link(self, ctx):
		await ctx.send("Join the support server at: https://discord.gg/hgQTTU7")

    @command(name="ping", brief="Shows the bot's latency.")
    @cooldown(1, 10, BucketType.user)
    async def ping(self, ctx):
        start = time()
        message = await ctx.send("Loading...")
        end = time()
        await message.edit(content=f"Pong! :ping_pong: Latency: {self.bot.latency*1000:,.0f} ms. Response time: {(end-start)*1000:,.0f} ms.")

    @command(name="shutdown", brief="Owner Only Command to shutdown the bot and save the DB.")
    async def shutdown(self, ctx):
        if ctx.author.id == owner_id:
            await ctx.send("Shutting down")

            db.commit()
            self.bot.scheduler.shutdown()
            await self.bot.logout()
        else:
            await ctx.send("You don't have permission to shutdown the bot.")

    @command(name="info", aliases=["botinfo"], brief="Gives basic info about Doob.")
    async def show_basic_bot_info(self, ctx):
        embed = Embed(title="Doob Info", colour=ctx.author.colour, timestamp=datetime.utcnow())

        bot_version = self.bot.VERSION

        fields = [("Name", "Doob", False),
                  ("Description", "A Discord bot made by mmatt using discord.py, he felt like making it so he did B)", False),
                  ("Developer", "The creator of Doob is <@308000668181069824>", False),
                  ("Doob's Server Count", f"{str(len(self.bot.guilds))}", True),
                  ("Doob's Member Count", f"{str(len(self.bot.users))}", True),
                  ("The ping for Doob is...", f" :ping_pong: {round(self.bot.latency * 1000)} ms", False),
                  ("Library", "discord.py", True),
                  ("Bot Version", f"{self.bot.VERSION} - [Changelog](https://github.com/doobdev/doob/blob/master/CHANGELOG.md#v{bot_version.replace('.', '')})", True),
                  ("Top.gg Link", "https://top.gg/bot/680606346952966177", False),
                  ("Invite Link", "[Invite Link Here](https://discordapp.com/oauth2/authorize?client_id=680606346952966177&scope=bot&permissions=271674430)", True),
                  ("GitHub Repository", "[Click Here](https://github.com/doobdev/doob)", True)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        embed.set_thumbnail(url=ctx.guild.me.avatar_url)
        embed.set_footer(text=f"{ctx.author.name} requested Doob's information", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("meta")

def setup(bot):
    bot.add_cog(Meta(bot))
