import logging
from discord.ext.commands import Cog

from ..db import db  # pylint: disable=relative-beyond-top-level

log = logging.getLogger()


class Welcome(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("welcome")

    @Cog.listener()
    async def on_member_join(self, member):
        db.execute("INSERT INTO users (UserID) VALUES (?)", member.id)
        log.info(f"{member.username} (member/user) have been added into the users DB")
        await db.execute(
            "INSERT INTO guildexp (UserID, GuildID) VALUES (?, ?)",
            member.id,
            member.guild.id,
        )
        log.info(
            f"{member.username} (member/user) have been added into the server exp DB"
        )
        await db.execute("INSERT INTO luckydogs (UserID) VALUES (?)", member.id)
        log.info(
            f"{member.username} (member/user) has been added into the LuckyDogs DB"
        )
        await db.execute(
            f"INSERT OR IGNORE INTO warns (UserID, GuildID) VALUES (?, ?)",
            member.id,
            member.guild.id,
        )
        log.info(f"{member.username} (member/user) has been added into the Warns DB.")
        await db.execute(f"INSERT OR IGNORE INTO globalwarns (UserID) VALUES (?)", member.id)
        log.info(
            f"{member.username} (member/user) have been added into the global warns DB."
        )
        await db.commit()

    @Cog.listener()
    async def on_guild_join(self, guild):
        await db.execute("INSERT INTO guilds (GuildID) VALUES (?)", guild.id)
        log.info(f"{guild.name} (guild) have been added into the DB")
        await db.multiexec(
            "INSERT OR IGNORE INTO users (UserID) VALUES (?)",
            ((member.id,) for member in guild.members if not member.bot),
        )
        log.info(f"{guild.name} users have been added into the users DB")
        await db.commit()

    @Cog.listener()
    async def on_message(self, message):
        if message.guild:
            return

        if message.content == "help":
            await message.author.send(
                "Type `@Doob help` in a server with @Doob to get a command list!\nSupport Server: https://discord.gg/hgQTTU7"
            )

        if message.content == "donate":
            await message.author.send("How generous!\nhttps://patreon.com/doobdev")

        else:
            await message.author.send(
                "Most commands can only be used in servers, not DMs!"
            )


def setup(bot):
    bot.add_cog(Welcome(bot))
