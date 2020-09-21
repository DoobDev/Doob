from datetime import datetime, timedelta
from random import randint
from typing import Optional

from discord import Member, Embed
from discord.ext.commands import Cog
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions
from discord.ext.menus import MenuPages, ListPageSource
from lib.bot import bot
from ..db import db # pylint: disable=relative-beyond-top-level

# daniel was here :o

class Menu(ListPageSource):
    def __init__(self, ctx, data):
        self.ctx = ctx
        self.bot = bot

        super().__init__(data, per_page=10)

    async def write_page(self, menu, offset, fields=[]):
        offset = (menu.current_page*self.per_page) + 1
        len_data = len(self.entries)

        embed = Embed(title="XP Leaderboard", description="See who is on top!", colour=self.ctx.author.colour)
        embed.set_thumbnail(url=self.ctx.guild.me.avatar_url)
        embed.set_footer(text=f"{offset:,} - {min(len_data, offset+self.per_page-1):,} of {len_data:,} members.")
        
        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)

        return embed

    async def format_page(self, menu, entries):
        offset = (menu.current_page*self.per_page) + 1
        fields = []
        table = ("\n".join(f"{idx+offset}. {bot.get_user(entry[0]).name} (XP: {entry[1]} | Level: {entry[2]})"
                   for idx, entry in enumerate(entries)))

        fields.append(("Ranks", table))

        return await self.write_page(menu, offset, fields)

class Exp(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def process_xp(self, message):
        xp, lvl, xplock = db.record("SELECT XP, Level, XPLock FROM exp WHERE UserID = ?", message.author.id)

        if datetime.utcnow() > datetime.fromisoformat(xplock):
            await self.add_xp(message, xp, lvl)

    async def add_xp(self, message, xp, lvl):
        xp_to_add = randint(10, 20)
        level_up_messages = db.record("SELECT LevelMessages FROM guilds WHERE GuildID = ?", message.guild.id)
        
        new_lvl = int(((xp + xp_to_add)//42) ** 0.55)

        db.execute("UPDATE exp SET XP = XP + ?, Level = ?, XPLock = ? WHERE UserID = ?", 
                   xp_to_add, new_lvl, (datetime.utcnow()+timedelta(seconds=50)).isoformat(), message.author.id)

        if new_lvl > lvl:
            if level_up_messages == "yes":
                await message.channel.send(f"{message.author.mention} leveled up to {new_lvl:,}!", delete_after = 10)

    @command(name="level", aliases=["rank", "lvl"], brief="Shows your level, and rank.")
    async def display_level(self, ctx, target: Optional[Member]):
        target = target or ctx.author

        ids = db.column("SELECT UserID FROM exp ORDER BY XP DESC")
        xp, lvl = db.record("SELECT XP, Level FROM exp WHERE UserID = ?", target.id) or (None, None)

        if lvl is not None:
            await ctx.send(f"{target.display_name} is level {lvl:,} with {xp:,} xp and is rank {ids.index(target.id)+1} of {len(ids):,} users globally.")

        else:
            ctx.send("That member is not in the XP Database.")

    @command(name="levelmessages", aliases=["slm", "lm", "setlevelmessages"], brief="Set the server's level messages")
    @has_permissions(manage_guild=True)
    async def set_level_messages(self, ctx, *, yes_or_no: str):
        """PLEASE, put 'no' ALL LOWERCASE if you DO NOT want level messages"""
        if not len(yes_or_no):
            await ctx.send("One or more required areguments are missing.")

        else:
            db.execute("UPDATE guilds SET LevelMessages = ? WHERE GuildID = ?", yes_or_no, ctx.guild.id)
            db.commit()
            await ctx.send(f"Level messages set to {yes_or_no}.")

    @command(name="leaderboard", aliases=["lb", "xplb"], brief="Show who's on top of the Doob XP Leaderboard!")
    async def display_leaderboard(self, ctx):
        records = db.records("SELECT UserID, XP, Level FROM exp ORDER BY XP DESC")

        menu = MenuPages(source=Menu(ctx, records), clear_reactions_after=True, timeout=100.0)
        await menu.start(ctx)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("exp")

    @Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            await self.process_xp(message)

def setup(bot):
    bot.add_cog(Exp(bot))