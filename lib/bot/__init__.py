from asyncio import sleep
from glob import glob

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import Embed, File
from discord.errors import HTTPException, Forbidden
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import Context, when_mentioned_or, command, has_permissions
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument, CommandOnCooldown)
import os
from ..db import db # pylint: disable=relative-beyond-top-level

OWNER_IDS = [308000668181069824]
COGS = [path.split(os.sep)[-1][:-3] for path in glob("./lib/cogs/*.py")]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)

def get_prefix(bot, message):
    prefix = db.field("SELECT Prefix FROM guilds WHERE GuildID = ?", message.guild.id)
    return when_mentioned_or(prefix)(bot, message)

class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f'{cog} cog ready')

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])

class Bot(BotBase):
    def __init__(self):
        self.ready = False
        self.cogs_ready = Ready()

        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)

        super().__init__(command_prefix=get_prefix, owner_ids=OWNER_IDS)

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"{cog} cog loaded!")

        print("Setup done!")

    def update_db(self):
        db.multiexec("INSERT OR IGNORE INTO guilds (GuildID) VALUES (?)",
                        ((guild.id,) for guild in self.guilds))
        db.commit()

    def run(self, version):
        self.VERSION = version

        print("Running setup!")
        self.setup()

        with open("./lib/bot/token.txt", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("Starting up")
        super().run(self.TOKEN, reconnect=True)

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)

        if ctx.command is not None and ctx.guild is not None:
            if self.ready:

                    await self.invoke(ctx)

            else:
                await ctx.send("Please wait, Doob hasn't fully started up yet", delete_after=10)

    async def on_connect(self):
        self.update_db()
        print("Doob Connected")
    
    async def on_disconnect(self):
        print("Doob Disconnected")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong. :/")

        raise err

    async def on_command_error(self, ctx, exc):
        if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
            pass
        
        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send("Required arguments missing.", delete_after = 10)

        elif isinstance(exc, CommandOnCooldown):
            await ctx.send(f'That command is on a {str(exc.cooldown.type).split(".")[-1]} cooldown! Try again in {exc.retry_after:,.2f} seconds.', delete_after = exc.retry_after)

        elif hasattr(exc, "original"):
            if isinstance(exc.original, HTTPException):
                await ctx.send("Unable to send message.", delete_after = 10)

            if isinstance(exc.original, Forbidden):
                await ctx.send("Doob doesn't have permissions in this server to use that command.", delete_after = 10)

            else:
                raise exc.original

        else:
            raise exc


    async def on_ready(self):
        if not self.ready:
            self.scheduler.start()
            while not self.cogs_ready.all_ready():
                await sleep(0.5)

            db.multiexec("INSERT OR IGNORE INTO exp (UserID) VALUES (?)",
                            ((member.id,) for guild in self.guilds for member in guild.members if not member.bot))

            self.ready = True
            self.update_db
            print("Doob Ready")

            meta = self.get_cog("Meta")
            await meta.set()

        else:
            print("Doob Reconnected")

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)

bot = Bot()