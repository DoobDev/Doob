from datetime import datetime, timedelta
from random import randint
from typing import Optional
from discord import Member, Embed
from discord.ext.commands import Cog
from discord.ext.commands import command, has_permissions
from discord.ext.menus import MenuPages, ListPageSource
from lib.bot import bot  # pylint: disable=no-name-in-module, import-error
from ..db import db  # pylint: disable=relative-beyond-top-level
from PIL import Image, ImageDraw, ImageFont


class Menu(ListPageSource):
    def __init__(self, ctx, data):
        self.ctx = ctx
        self.bot = bot

        super().__init__(data, per_page=10)

    async def write_page(self, menu, offset, fields=[]):
        offset = (menu.current_page * self.per_page) + 1
        len_data = len(self.entries)

        embed = Embed(
            title="Global XP Leaderboard",
            description="See who is on top!",
            colour=self.ctx.author.colour,
        )
        embed.set_author(
            name="Warning ⚠: Global XP leaderboard is super slow at the moment."
        )
        embed.set_thumbnail(url=self.ctx.guild.me.avatar_url)
        embed.set_footer(
            text=f"{offset:,} - {min(len_data, offset+self.per_page-1):,} of {len_data:,} members."
        )

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)

        return embed

    async def format_page(self, menu, entries):
        offset = (menu.current_page * self.per_page) + 1
        fields = []
        table = "\n".join(
            f"{idx+offset}. {bot.get_user(entry[0]).name} (XP: {entry[1]} | Level: {entry[2]})"
            for idx, entry in enumerate(entries)
        )

        fields.append(("Ranks", table))

        return await self.write_page(menu, offset, fields)


class ServerMenu(ListPageSource):
    def __init__(self, ctx, data):
        self.ctx = ctx
        self.bot = bot

        super().__init__(data, per_page=10)

    async def write_page(self, menu, offset, fields=[]):
        offset = (menu.current_page * self.per_page) + 1
        len_data = len(self.entries)

        embed = Embed(
            title="Server XP Leaderboard",
            description="See who is on top!",
            colour=self.ctx.author.colour,
        )
        embed.set_thumbnail(url=self.ctx.guild.icon_url)
        embed.set_footer(
            text=f"{offset:,} - {min(len_data, offset+self.per_page-1):,} of {len_data:,} members."
        )

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)

        return embed

    async def format_page(self, menu, entries):
        offset = (menu.current_page * self.per_page) + 1
        fields = []
        table = "\n".join(
            f"{idx+offset}. {bot.get_user(entry[0]).display_name} (XP: {entry[1]} | Level: {entry[2]})"
            for idx, entry in enumerate(entries)
        )

        fields.append(("Ranks", table))

        return await self.write_page(menu, offset, fields)


class Exp(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def process_xp(self, message):
        xp, lvl, xplock = db.record(
            "SELECT XP, Level, XPLock FROM users WHERE UserID = ?", message.author.id
        )
        xp_g, lvl_g, xplock_g = db.record(
            f"SELECT XP, Level, XPLock FROM guildexp WHERE UserID = {message.author.id} AND GuildID = {message.guild.id}"
        )

        if datetime.utcnow() > datetime.fromisoformat(xplock):
            await self.add_xp(message, xp, lvl)

        if datetime.utcnow() > datetime.fromisoformat(xplock_g):
            await self.add_gxp(message, xp_g, lvl_g)

    async def add_xp(self, message, xp, lvl):
        xp_to_add = randint(10, 20)
        level_up_messages = db.record(
            "SELECT LevelMessages FROM guilds WHERE GuildID = ?", message.guild.id
        )

        new_lvl = int(((xp + xp_to_add) // 42) ** 0.55)

        db.execute(
            "UPDATE users SET XP = XP + ?, Level = ?, XPLock = ? WHERE UserID = ?",
            xp_to_add,
            new_lvl,
            (datetime.utcnow() + timedelta(seconds=50)).isoformat(),
            message.author.id,
        )

        if new_lvl > lvl:
            if level_up_messages == "('yes',)" or level_up_messages == "('Yes',)":
                await message.channel.send(
                    f"{message.author.mention} leveled up to {new_lvl:,}!",
                    delete_after=10,
                )

    async def add_gxp(self, message, xp, lvl):
        xp_to_add = randint(10, 20)
        level_up_messages = db.record(
            "SELECT LevelMessages FROM guilds WHERE GuildID = ?", message.guild.id
        )

        new_lvl = int(((xp + xp_to_add) // 42) ** 0.55)

        db.execute(
            f"UPDATE guildexp SET XP = XP + ?, Level = ?, XPLock = ? WHERE UserID = {message.author.id} AND GuildID = {message.guild.id}",
            xp_to_add,
            new_lvl,
            (datetime.utcnow() + timedelta(seconds=50)).isoformat(),
        )
        db.commit()

        if new_lvl > lvl:
            if level_up_messages == "('yes',)" or level_up_messages == "('Yes',)":
                await message.channel.send(
                    f"{message.author.mention} leveled up to server level {new_lvl:,}!",
                    delete_after=10,
                )

    @commands.command()
    async def rank(self, ctx, target: Optional[Member]):
        await log.cog_command(self, ctx)
        target = target or context.author

        exp, level = db.record(f"SELECT XP, Level FROM users WHERE (guildID, UserID) = (?, ?)",
            target.guild.id,
            target.id
        )
        ids = db.column(f"SELECT UserID FROM users WHERE GuildID = {target.guild.id} ORDER BY XP DESC")


        if exp or level is not None:
            async with ctx.typing():
                await asyncio.sleep(1)

                rank = f"{ids.index(target.id)+1}"
                final_xp = 1000#this is where the formula i opened the issue would make a lot of sense. In my testing i was not able to get that to work though. 
                xp = exp
                user_name = str(target.name)
                discriminator = f"#{target.discriminator}"
                Level = int(((exp) // 42) ** 0.55)

                background = Image.new("RGB", (1000, 240))
                async with aiohttp.ClientSession() as session:
                    async with session.get(str(target.avatar_url)) as response:
                        image = await response.read()
                        icon = Image.open(BytesIO(image)).convert("RGBA").resize((200, 200))
                        bigsize = (icon.size[0] * 3, icon.size[1] * 3)
                        mask = Image.new("L", bigsize, 0)
                        draw = ImageDraw.Draw(mask)
                        draw.ellipse((0, 0) + bigsize, 255)
                        draw.ellipse((140 * 3, 140 * 3, 189 * 3, 189 * 3), 0)
                        mask = mask.resize(icon.size, Image.ANTIALIAS)
                        icon.putalpha(mask)
                        background.paste(icon, (20, 20), mask=icon)
                        draw = ImageDraw.Draw(background, "RGB")
                        draw.ellipse((162, 162, 206, 206), fill="#43B581")
                        big_font = ImageFont.FreeTypeFont("./lib/fonts/ABeeZee-Regular.otf", 60)
                        medium_font = ImageFont.FreeTypeFont("./lib/fonts/ABeeZee-Regular.otf", 40)
                        small_font = ImageFont.FreeTypeFont("./lib/fonts/ABeeZee-Regular.otf", 30)
                        text_size = draw.textsize(str(level), font=big_font)
                        offset_x = 1000 - 15 - text_size[0]
                        offset_y = 10
                        draw.text((offset_x, offset_y), str(level), font=big_font, fill="#11ebf2")
                        text_size = draw.textsize("LEVEL", font=small_font)
                        offset_x -= text_size[0] + 5
                        draw.text((offset_x, offset_y + 27), "LEVEL", font=small_font, fill="#11ebf2")
                        text_size = draw.textsize(f"#{rank}", font=big_font)
                        offset_x -= text_size[0] + 15
                        draw.text((offset_x, offset_y), f"#{rank}", font=big_font, fill="#fff")
                        text_size = draw.textsize("RANK", font=small_font)
                        offset_x -= text_size[0] + 5
                        draw.text((offset_x, offset_y + 27), "RANK", font=small_font, fill="#fff")
                        bar_offset_x = 320
                        bar_offset_y = 160
                        bar_offset_x_1 = 950
                        bar_offset_y_1 = 200
                        circle_size = bar_offset_y_1 - bar_offset_y
                        draw.rectangle((bar_offset_x, bar_offset_y, bar_offset_x_1, bar_offset_y_1), fill="#727175")
                        draw.ellipse(
                            (bar_offset_x - circle_size // 2, bar_offset_y, bar_offset_x + circle_size // 2, bar_offset_y_1), fill="#727175"
                        )
                        draw.ellipse(
                            (bar_offset_x_1 - circle_size // 2, bar_offset_y, bar_offset_x_1 + circle_size // 2, bar_offset_y_1), fill="#727175"
                        )
                        bar_length = bar_offset_x_1 - bar_offset_x
                        progress = (final_xp - xp) * 100 / final_xp
                        progress = 100 - progress
                        progress_bar_length = round(bar_length * progress / 100)
                        bar_offset_x_1 = bar_offset_x + progress_bar_length
                        draw.rectangle((bar_offset_x, bar_offset_y, bar_offset_x_1, bar_offset_y_1), fill="#11ebf2")
                        draw.ellipse(
                            (bar_offset_x - circle_size // 2, bar_offset_y, bar_offset_x + circle_size // 2, bar_offset_y_1), fill="#11ebf2"
                        )
                        draw.ellipse(
                            (bar_offset_x_1 - circle_size // 2, bar_offset_y, bar_offset_x_1 + circle_size // 2, bar_offset_y_1), fill="#11ebf2"
                        )
                        text_size = draw.textsize(f"/ {final_xp} XP", font=small_font)
                        offset_x = 950 - text_size[0]
                        offset_y = bar_offset_y - text_size[1] - 10
                        draw.text((offset_x, offset_y), f"/ {final_xp:,} XP", font=small_font, fill="#727175")
                        text_size = draw.textsize(f"{xp:,}", font=small_font)
                        offset_x -= text_size[0] + 8
                        draw.text((offset_x, offset_y), f"{xp:,}", font=small_font, fill="#fff")
                        text_size = draw.textsize(user_name, font=medium_font)
                        offset_x = bar_offset_x
                        offset_y = bar_offset_y - text_size[1] - 5
                        draw.text((offset_x, offset_y), user_name, font=medium_font, fill="#fff")
                        offset_x += text_size[0] + 5
                        offset_y += 10
                        draw.text((offset_x, offset_y), discriminator, font=small_font, fill="#727175")
                        background.show()
                        background.save("./images/imgswap.png")
                        ffile = discord.File("./images/imgswap.png")
                        await context.channel.send(file=ffile)

        else:
            await ctx .reply("You are not in the database :(\nDont worry though, you were just added! Try running the command again.", mention_author=False)

    @command(
        name="levelmessages",
        aliases=["slm", "lm", "setlevelmessages"],
        brief="Set the server's level messages",
    )
    @has_permissions(manage_guild=True)
    async def set_level_messages(self, ctx, *, yes_or_no: Optional[str]):
        """PLEASE, put 'yes' if you DO want level messages\n`Manage Server` permission required."""
        levelmessages = db.records(
            "SELECT LevelMessages FROM guilds WHERE GuildID = ?", ctx.guild.id
        ) or (None)
        prefix = db.records("SELECT Prefix FROM guilds WHERE GuildID = ?", ctx.guild.id)

        if (
            yes_or_no == "Yes"
            or yes_or_no == "yes"
            or yes_or_no == "no"
            or yes_or_no == "No"
        ):
            db.execute(
                "UPDATE guilds SET LevelMessages = ? WHERE GuildID = ?",
                yes_or_no,
                ctx.guild.id,
            )
            db.commit()
            await ctx.reply(f"Level messages set to `{yes_or_no}`.")

        else:
            await ctx.reply(
                f"The current setting for Level Messages is: `{levelmessages[0][0]}`\nTo change it, type `{prefix[0][0]}levelmessages (yes or no)`"
            )

    @command(
        name="leaderboard",
        aliases=["lb", "xplb"],
        brief="Show who's on top of the Doob GlobalXP Leaderboard!",
    )
    async def display_leaderboard(self, ctx):
        """Displays the Global XP Leaderboard for Doob."""
        records = db.records("SELECT UserID, XP, Level FROM users ORDER BY XP DESC")

        menu = MenuPages(
            source=Menu(ctx, records), clear_reactions_after=True, timeout=100.0
        )
        await menu.start(ctx)

    @command(
        name="serverleaderboard",
        aliases=["serverlb", "serverxplb", "svxp", "svxplb"],
        brief="Show who's on top of the Doob ServerXP Leaderboard!",
    )
    async def display_serverxp_leaderboard(self, ctx):
        """Displays the Server XP Leaderboard for Doob."""
        records = db.records(
            "SELECT UserID, XP, Level FROM guildexp WHERE GuildID = ? ORDER BY XP DESC",
            ctx.guild.id,
        )

        menu = MenuPages(
            source=ServerMenu(ctx, records), clear_reactions_after=True, timeout=100.0
        )
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
