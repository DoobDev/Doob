from asyncio import sleep

from glob import glob

import discord
from discord import Embed, Colour, Client, Intents

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.errors import Forbidden
from pathlib import Path

from discord.ext.commands import Bot as BotBase
from discord.ext.commands import Context, when_mentioned_or, has_permissions
from discord.ext.commands import (
    CommandNotFound,
    BadArgument,
    MissingRequiredArgument,
    CommandOnCooldown,
    MissingPermissions,
    EmojiNotFound,
    NotOwner,
)

import os

from discord_slash import SlashCommand

from ..db import db  # pylint: disable=relative-beyond-top-level

from dotenv import load_dotenv

import json

with open("config.json") as config_file:
    config = json.load(config_file)

cwd = Path(__file__).parents[0]
cwd = str(cwd)

# Loads the .env file from ./.env
load_dotenv()

# Put Owner's Discord IDs into the list below
OWNER_IDS = config["owner_ids"]
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
        return all(getattr(self, cog) for cog in COGS)


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
            case_insensitive=True,
            help_command=None,
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

        # The following "fmt" comments are so that black, Doob's code style of choice, doesn't touch this line, if black touches it, then some Ubuntu machines can't run the bot.

        # fmt: off
        super().run(os.environ.get('TOKEN'), reconnect=True)
        # fmt: on

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)

        if ctx.command is not None and ctx.guild is not None:
            if self.ready:
                await self.invoke(ctx)

            else:
                await ctx.reply(
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
            raise err

    # Basic error handling for Doob
    async def on_command_error(self, ctx, exc):
        # if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
        #     await ctx.reply(
        #         f"Something went wrong!\n\nError: {exc.original}", delete_after=10
        #     )

        if isinstance(exc, MissingRequiredArgument):
            await ctx.reply("Required arguments missing.", delete_after=10)

        elif isinstance(exc, CommandOnCooldown):
            await ctx.reply(
                f'That command is on a {str(exc.cooldown.type).split(".")[-1]} cooldown! Try again in {exc.retry_after:,.2f} seconds.',
                delete_after=exc.retry_after,
            )

        elif isinstance(exc, MissingPermissions):
            await ctx.reply("You don't have permissions for that.", delete_after=10)

        elif isinstance(exc, EmojiNotFound):
            await ctx.reply(
                "This emote could not be found. This is likely because Doob isn't in the same server as this emote.",
                delete_after=10,
            )

        elif isinstance(exc, NotOwner):
            await ctx.reply(
                "This command is only available to the bot owner.",
                delete_after=10,
            )

        elif hasattr(exc, "original"):
            if isinstance(exc.original, Forbidden):
                await ctx.reply(
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

            # db.multiexec(f"INSERT OR IGNORE INTO globalwarns (UserID) VALUES (?)", member.id)
            db.multiexec(
                "INSERT OR IGNORE INTO globalwarns (UserID) VALUES (?)",
                (
                    (member.id,)
                    for guild in self.guilds
                    for member in guild.members
                    if not member.bot
                ),
            )
            print("Updated global warns table.")

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
        def read_json(filename):
            with open(f"./lib/cogs/{filename}.json", "r") as file:
                data = json.load(file)
            return data

        blacklisted_users = read_json("blacklisted_users")

        if (
            not message.author.bot
            and message.author.id not in blacklisted_users["blacklist"]
        ):
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

            db.execute(
                f"INSERT OR IGNORE INTO warns (UserID, GuildID) VALUES (?, ?)",
                message.author.id,
                message.guild.id,
            )
            db.execute(
                f"INSERT OR IGNORE INTO globalwarns (UserID) VALUES (?)",
                message.author.id,
            )

            db.commit()

        if message.author.id in blacklisted_users[
            "blacklist"
        ] and message.content.startswith(
            db.field("SELECT Prefix FROM guilds WHERE GuildID = ?", message.guild.id)
        ):
            await message.channel.send(
                "You are blacklisted from using Doob commands.", delete_after=10
            )


bot = Bot()
bot.load_extension("jishaku")
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)
