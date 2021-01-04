from asyncio import sleep

from glob import glob

import discord
from discord import Embed, Colour, Client, Intents

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from discord.errors import Forbidden

from discord.ext.commands import Bot as BotBase
from discord.ext.commands import Context, when_mentioned_or, has_permissions
from discord.ext.commands import (
    CommandNotFound,
    BadArgument,
    MissingRequiredArgument,
    CommandOnCooldown,
)

import os

from ..db import db  # pylint: disable=relative-beyond-top-level

from dotenv import load_dotenv

# Loads the .env file from ./.env
load_dotenv()

# Put Owner's Discord IDs into the list below
OWNER_IDS = [308000668181069824]
# Loads the cogs from the path
COGS = [path.split(os.sep)[-1][:-3] for path in glob("./lib/cogs/*.py")]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)

# Gets the prefix from the DB
def get_prefix(bot, message):
    prefix = db.field("SELECT Prefix FROM guilds WHERE GuildID = ?", message.guild.id)
    return when_mentioned_or(prefix)(bot, message)


class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"{cog} cog ready")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
    def __init__(self):
        self.ready = False
        self.cogs_ready = Ready()

        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)

        # Gives access to Discord's intents.
        # If you have a bot with over 75 servers, you will need to get whitelisted to use these. If not, you can enable them in your developer dashboard at https://discord.dev
        intents = discord.Intents.default()
        intents.members = True
        intents.presences = False

        super().__init__(
            command_prefix=get_prefix,
            owner_ids=OWNER_IDS,
            chunk_guilds_at_startup=True,
            intents=intents,
            case_insensitive=True
        )

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"[COGS] {cog} cog loaded!")

        print("Setup done!")

    def update_db(self):
        db.multiexec(
            "INSERT OR IGNORE INTO guilds (GuildID) VALUES (?)",
            ((guild.id,) for guild in self.guilds),
        )
        db.commit()

    def run(self, version):
        self.VERSION = version

        print("Running setup!")
        self.setup()
        print("Authenticated...")
        print("Starting up")
        # Gets the token from the .env to authenticate the bot.
        super().run(os.environ.get("TOKEN"), reconnect=True)

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)

        if ctx.command is not None and ctx.guild is not None:
            if self.ready:
                await self.invoke(ctx)

            else:
                await ctx.send(
                    "Please wait, Doob hasn't fully started up yet <a:loadingdoob:755141175840866364>",
                    delete_after=10,
                )

    async def on_connect(self):
        self.update_db()
        print("Doob Connected")

    async def on_disconnect(self):
        print("Doob Disconnected")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":

            # embed = Embed(title="Oops!", description="This command didn't work correctly.", colour=Colour.red())
            # embed.add_field(name="❓ Join the Support Server:", value="https://discord.gg/hgQTTU7")
            # await args[0].send(embed=embed)
            
            raise err

    # Basic error handling for Doob
    async def on_command_error(self, ctx, exc):
        if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
            await ctx.send(
                f"Something went wrong!\n\nError: {exc.original}", delete_after=10
            )

        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send("Required arguments missing.", delete_after=10)

        elif isinstance(exc, CommandOnCooldown):
            await ctx.send(
                f'That command is on a {str(exc.cooldown.type).split(".")[-1]} cooldown! Try again in {exc.retry_after:,.2f} seconds.',
                delete_after=exc.retry_after,
            )

        elif hasattr(exc, "original"):
            if isinstance(exc.original, Forbidden):
                await ctx.send(
                    "Doob doesn't have permissions to do that.", delete_after=10
                )

            else:
                raise exc.original

        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.scheduler.start()
            while not self.cogs_ready.all_ready():
                await sleep(1.0)

            # Puts all users into the users DB
            db.multiexec(
                "INSERT OR IGNORE INTO users (UserID) VALUES (?)",
                (
                    (member.id,)
                    for guild in self.guilds
                    for member in guild.members
                    if not member.bot
                ),
            )
            print("Updated users table.")

            # Puts all users in the votes DB
            db.multiexec(
                "INSERT OR IGNORE INTO votes (UserID) VALUES (?)",
                (
                    (member.id,)
                    for guild in self.guilds
                    for member in guild.members
                    if not member.bot
                ),
            )
            print("Updated votes table.")

            self.ready = True
            self.update_db

            print("Updated DB")
            print("Doob Ready")

            meta = self.get_cog("Meta")
            await meta.set()

        else:
            print("Doob Reconnected")

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)
            # If someone types a message, then they get inserted into the guildexp and luckydogs DB
            db.execute(
                "INSERT OR IGNORE INTO guildexp (UserID, GuildID) VALUES (?, ?)",
                message.author.id,
                message.guild.id,
            )
            db.execute(
                "INSERT OR IGNORE INTO luckydogs (UserID) VALUES (?)", message.author.id
            )
            db.commit()


bot = Bot()
