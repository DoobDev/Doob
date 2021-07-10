from random import choice, randint, random
from typing import Optional
from aiohttp import request
from datetime import datetime
from asyncio import sleep

from discord import Member, Embed, Colour
from discord.ext.commands import Cog, command, cooldown, BucketType, group
from discord.utils import get
from discord_slash import cog_ext

from owoify import Owoifator

owoifactor = Owoifator()

from ..db import db  # pylint: disable=relative-beyond-top-level

import json

with open("config.json") as config_file:
    config = json.load(config_file)


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="hello", aliases=["hi"], brief="Say Hi to Doob!")
    async def say_hello(self, ctx):
        """Say Hi to Doob!"""
        # Chooses Hello, Hi, or Hey at random, to say Hi to the user.
        await ctx.reply(f"{choice(('Hello', 'Hi', 'Hey'))} {ctx.author.mention}!")

    @command(name="dice", aliases=["roll", "rolldice"], brief="Roll some dice!")
    @cooldown(1, 10, BucketType.user)
    async def roll_dice(self, ctx, die_string: str):
        """Role some dice, (number)d(number) syntax."""
        dice, value = (int(term) for term in die_string.split("d"))

        # If the dice is less or equal to 40, then run the command
        if dice <= 40:
            rolls = [randint(1, value) for i in range(dice)]

            await ctx.reply(" + ".join([str(r) for r in rolls]) + f" = {sum(rolls)}")

        # If the dice number is too high, we don't run the command
        # This is because higher then 40 dice can lead to errors regarding message length.
        else:
            await ctx.reply("Please roll a lower number of dice.", delete_after=10)

    @command(name="echo", aliases=["say"], brief="Make Doob say something!")
    async def echo_message(self, ctx, *, message):
        """Make Doob say a message! | `Patreon Only`"""
        homeGuild = self.bot.get_guild(config["homeGuild_id"])  # Support Server ID.
        patreonRole = get(
            homeGuild.roles, id=config["patreonRole_id"]
        )  # Patreon role ID.

        member = []

        # Checks if a user is a Patreon member.
        for pledger in homeGuild.members:
            if pledger == ctx.author:
                member = pledger

        if ctx.author in homeGuild.members:
            if patreonRole in member.roles:
                # If they are, run the command.
                await ctx.message.delete()
                await ctx.send(message)
                print(f"{ctx.author.name} used the Echo command and said {message}")

            # This else is for if they are in the server, but not a Patron
            else:
                await ctx.reply(
                    "You are not a Patron to Doob, subscribe to any of the tiers at <https://patreon.com/doobdev> to gain access to this command."
                )

        # This else is for if they aren't in the server, and are not a Patreon (you can only get Patron benefits by joining the Support Server)
        else:
            await ctx.reply(
                "You are not a Patron to Doob, subscribe to any of the tiers at <https://patreon.com/doobdev> to gain access to this command."
            )

    @command(
        name="fact",
        aliases=["dogfact", "facts"],
        brief="Learn a random fact about dogs!",
    )
    @cooldown(3, 10, BucketType.user)
    async def dog_fact(self, ctx):
        """Get a wacky dog fact"""
        # URL of the API
        URL = "https://some-random-api.ml/facts/dog"

        # GETs a json response from URL, puts the fact into an embed, then sends it to the user.
        async with request("GET", URL, headers={}) as response:
            if response.status == 200:
                data = (
                    await response.json()
                )  # Right here is where it gets the data from the json response.
                embed = Embed(
                    title="Dog Fact!",
                    description=data["fact"],
                    colour=ctx.author.colour,
                )
                embed.set_footer(
                    text=f"{ctx.author} requested this fact!",
                    icon_url=ctx.author.avatar_url,
                )
                await ctx.reply(embed=embed)
            else:
                # if the API responds with a status not being "200" (200=Working just fine), sends out an error message to the user with the status number.
                await ctx.reply(f"Dog fact API sent a {response.status} status.")

    @command(name="luckydog", aliases=["ldog"], brief="Get an instant Lucky Dog!")
    @cooldown(2, 5, BucketType.user)
    async def lucky_dog_image(self, ctx, *, dog: Optional[str]):
        """Shows the lucky dogs possible!\nIsn't eligable for the Nitro Giveaways\n`Patreon` permission required"""
        homeGuild = self.bot.get_guild(config["homeGuild_id"])  # Support Server ID.
        patreonRole = get(
            homeGuild.roles, id=config["patreonRole_id"]
        )  # Patreon role ID.

        member = []

        # Checks if someone is a Patron
        for pledger in homeGuild.members:
            if pledger == ctx.author:
                member = pledger

        # If they are, let them run the command
        if ctx.author in homeGuild.members:
            if patreonRole in member.roles:
                if dog == "1":
                    embed = Embed(
                        title="Lucky Dog Picture!",
                        description="This is [Liquid Mendo](https://twitter.com/Mendo)'s dog Koda!",
                        colour=Colour.gold(),
                    )
                    embed.set_footer(
                        text=f"{ctx.author} got this lucky dog picture!",
                        icon_url=ctx.author.avatar_url,
                    )
                    embed.set_image(
                        url="https://pbs.twimg.com/media/EgXfe_XUcAABT41?format=jpg&name=360x360"
                    )
                    await ctx.reply(embed=embed)

                elif dog == "2":
                    embed = Embed(
                        title="Lucky Dog Picture!",
                        description="You selected the old `GAMING` server PFP!",
                        colour=Colour.gold(),
                    )
                    embed.set_footer(
                        text=f"Thanks for supporting Doob, {ctx.author.name}!",
                        icon_url=ctx.author.avatar_url,
                    )
                    embed.set_image(url="https://i.imgur.com/pzqRLdi.jpg")
                    await ctx.reply(embed=embed)

                elif dog == "3":
                    embed = Embed(
                        title="Lucky Dog Picture!",
                        description="This is [Weest](https://twitter.com/weesterner)'s dog Kevin!",
                        colour=Colour.gold(),
                    )
                    embed.set_footer(
                        text=f"Thanks for supporting Doob, {ctx.author.name}!",
                        icon_url=ctx.author.avatar_url,
                    )
                    embed.set_image(url="https://i.imgur.com/guF2Y3z.png")
                    await ctx.reply(embed=embed)

                elif dog == "4":
                    embed = Embed(
                        title="Lucky Dog Picture!",
                        description="This is [@KittyKay000](https://twitter.com/kittykay000)'s concept drawing of Doob!",
                        colour=Colour.gold(),
                    )
                    embed.set_footer(
                        text=f"Thanks for supporting Doob, {ctx.author.name}!",
                        icon_url=ctx.author.avatar_url,
                    )
                    embed.set_image(url="https://i.imgur.com/KFOR8YJ.jpeg")
                    await ctx.reply(embed=embed)

                else:
                    embed = Embed(
                        title="Lucky Dogs Possible:",
                        description="1 = [Liquid Mendo](https://twitter.com/mendo)'s dog Koda\n2 = Old `GAMING` server PFP\n3 = [Weest](https://twitter.com/weesterner)'s dog Kevin\n4 = [@KittyKay000](https://twitter.com/kittykay000)'s concept drawing for Doob!",
                        colour=ctx.author.colour,
                    )
                    embed.set_footer(
                        text=f"Thanks for supporting Doob, {ctx.author.name}!",
                        icon_url=ctx.author.avatar_url,
                    )
                    await ctx.reply(embed=embed)

            # Refer to line 59 and 63 for reasoning on the bottom 2 elses.
            else:
                await ctx.reply(
                    "This is a Patreon (<https://patreon.com/doobdev>) only command."
                )

        else:
            await ctx.reply(
                "This is a Patreon (<https://patreon.com/doobdev>) only command."
            )

    @command(
        name="luckydogs",
        aliases=["dogscaught", "ldc", "ld", "checkdogs", "lds"],
        brief="Check how many Lucky Dogs you have gotten!",
    )
    @cooldown(2, 5, BucketType.user)
    async def check_lucky_dogs(self, ctx, *, target: Optional[Member]):
        """Check how many Lucky dogs you have gotten in the last month!"""
        target = target or ctx.author

        # Pulls from the database how many luckydogs a user has.
        LuckyDogs = db.records(
            "SELECT LuckyDogs FROM luckydogs WHERE UserID = ?", target.id
        )

        # Gives how many lucky dogs a user has.
        embed = Embed(
            title=f"{target.name} has gotten:",
            description=f"{str(LuckyDogs[0][0])} Lucky Dog(s) this month.",
            colour=target.colour,
        )
        embed.set_footer(
            text=f"{ctx.author.name} requested this. | Doob",
            icon_url=ctx.author.avatar_url,
        )
        embed.set_thumbnail(url=target.avatar_url)
        await ctx.reply(embed=embed)

    @command(name="dog", aliases=["dogimage"], brief="See a random picture of a dog!")
    @cooldown(2, 5, BucketType.user)
    async def dog_image(self, ctx):
        """So this is what you came for...\nGives you a random picture of a dog!"""
        LuckyDogs = db.records(
            "SELECT LuckyDogs FROM luckydogs WHERE UserID = ?", ctx.author.id
        )

        homeGuild = self.bot.get_guild(config["homeGuild_id"])  # Support Server ID.
        patreonRole = get(
            homeGuild.roles, id=config["patreonRole_id"]
        )  # Patreon role ID.

        member = []

        # URL for the API
        URL = "https://dog.ceo/api/breeds/image/random"

        # Checks if user is a Patron
        for pledger in homeGuild.members:
            if pledger == ctx.author:
                member = pledger

        # If the user is, give them a higher chance in the Lucky Dog Rolls
        if ctx.author in homeGuild.members:
            if patreonRole in member.roles:

                # Rolls a random number between 1 and 53 for Patrons, to give them a higher chance of getting a "Lucky Dog"
                random = randint(1, 53)

                # If the user doesn't get a lucky dog roll, then contact the API and get a picture!
                if random != 50 and random != 51 and random != 52 and random != 53:
                    async with request("GET", URL, headers={}) as response:
                        if response.status == 200:
                            data = await response.json()
                            embed = Embed(
                                title="Dog Picture!", colour=ctx.author.colour
                            )
                            # embed.set_footer(text=f"DEBUG: L_DOG: {random}")
                            embed.set_image(url=data["message"])
                            await ctx.reply(embed=embed)

                # This is the Lucky Dog stuff, if the user rolls one of these numbers, they get a "Lucky Dog", that gives them the special dog
                # and gives them 1 "Lucky Dog" into the DB
                elif random == 50:
                    embed = Embed(
                        title="Lucky Dog Picture!",
                        description="This is [Liquid Mendo](https://twitter.com/Mendo)'s dog Koda!",
                        colour=Colour.gold(),
                    )
                    embed.set_footer(
                        text=f"{ctx.author} got this lucky dog picture! | There is a 1 in 50 chance of getting this picture!",
                        icon_url=ctx.author.avatar_url,
                    )
                    embed.set_image(
                        url="https://pbs.twimg.com/media/EgXfe_XUcAABT41?format=jpg&name=360x360"
                    )
                    db.execute(
                        "UPDATE luckydogs SET (LuckyDogs, LastUpdated) = (?, ?) WHERE UserID = ?",
                        LuckyDogs[0][0] + 1,
                        datetime.utcnow(),
                        ctx.author.id,
                    )
                    await ctx.reply(embed=embed)

                elif random == 51:
                    embed = Embed(
                        title="Lucky Dog Picture!",
                        description="There is a 1 in 50 chance of getting this picture!",
                        colour=Colour.gold(),
                    )
                    embed.set_footer(
                        text=f"{ctx.author} got this lucky dog picture!",
                        icon_url=ctx.author.avatar_url,
                    )
                    embed.set_image(url="https://i.imgur.com/pzqRLdi.jpg")
                    db.execute(
                        "UPDATE luckydogs SET (LuckyDogs, LastUpdated) = (?, ?) WHERE UserID = ?",
                        LuckyDogs[0][0] + 1,
                        datetime.utcnow(),
                        ctx.author.id,
                    )
                    await ctx.reply(embed=embed)

                elif random == 52:
                    embed = Embed(
                        title="Lucky Dog Picture!",
                        description="This is [Weest](https://twitter.com/weesterner)'s dog Kevin!",
                        colour=Colour.gold(),
                    )
                    embed.set_footer(
                        text=f"{ctx.author} got this lucky dog picture! | There is a 1 in 50 chance of getting this picture!",
                        icon_url=ctx.author.avatar_url,
                    )
                    embed.set_image(url="https://i.imgur.com/guF2Y3z.png")
                    db.execute(
                        "UPDATE luckydogs SET (LuckyDogs, LastUpdated) = (?, ?) WHERE UserID = ?",
                        LuckyDogs[0][0] + 1,
                        datetime.utcnow(),
                        ctx.author.id,
                    )
                    await ctx.reply(embed=embed)

                elif random == 53:
                    embed = Embed(
                        title="Lucky Dog Picture!",
                        description="This is [@KittyKay000](https://twitter.com/kittykay000)'s concept drawing of Doob!",
                        colour=Colour.gold(),
                    )
                    embed.set_footer(
                        text=f"{ctx.author} got this lucky dog picture! | There is a 1 in 50 chance of getting this picture!",
                        icon_url=ctx.author.avatar_url,
                    )
                    embed.set_image(url="https://i.imgur.com/KFOR8YJ.jpeg")
                    db.execute(
                        "UPDATE luckydogs SET (LuckyDogs, LastUpdated) = (?, ?) WHERE UserID = ?",
                        LuckyDogs[0][0] + 1,
                        datetime.utcnow(),
                        ctx.author.id,
                    )
                    await ctx.reply(embed=embed)

            else:
                # If they aren't a Patron, it calls the function below.
                await self.lucky_dogs(ctx)

        else:
            # If they aren't in the support server, it calls the function below.
            await self.lucky_dogs(ctx)

    @cog_ext.cog_slash(name="dog", description="See a random picture of a dog!")
    async def dog_slash_command(self, SlashContext):
        ctx = SlashContext

        LuckyDogs = db.records(
            "SELECT LuckyDogs FROM luckydogs WHERE UserID = ?", ctx.author.id
        )

        homeGuild = self.bot.get_guild(config["homeGuild_id"])  # Support Server ID.
        patreonRole = get(
            homeGuild.roles, id=config["patreonRole_id"]
        )  # Patreon role ID.

        member = []

        # URL for the API
        URL = "https://dog.ceo/api/breeds/image/random"

        # Checks if user is a Patron
        for pledger in homeGuild.members:
            if pledger == ctx.author:
                member = pledger

        # If the user is, give them a higher chance in the Lucky Dog Rolls
        if ctx.author in homeGuild.members:
            if patreonRole in member.roles:

                # Rolls a random number between 1 and 53 for Patrons, to give them a higher chance of getting a "Lucky Dog"
                random = randint(1, 53)

                # If the user doesn't get a lucky dog roll, then contact the API and get a picture!
                if random != 50 and random != 51 and random != 52 and random != 53:
                    async with request("GET", URL, headers={}) as response:
                        if response.status == 200:
                            data = await response.json()
                            embed = Embed(
                                title="Dog Picture!", colour=ctx.author.colour
                            )
                            # embed.set_footer(text=f"DEBUG: L_DOG: {random}")
                            embed.set_image(url=data["message"])
                            await ctx.send(embed=embed)

                # This is the Lucky Dog stuff, if the user rolls one of these numbers, they get a "Lucky Dog", that gives them the special dog
                # and gives them 1 "Lucky Dog" into the DB
                elif random == 50:
                    embed = Embed(
                        title="Lucky Dog Picture!",
                        description="This is [Liquid Mendo](https://twitter.com/Mendo)'s dog Koda!",
                        colour=Colour.gold(),
                    )
                    embed.set_footer(
                        text=f"{ctx.author} got this lucky dog picture! | There is a 1 in 50 chance of getting this picture!",
                        icon_url=ctx.author.avatar_url,
                    )
                    embed.set_image(
                        url="https://pbs.twimg.com/media/EgXfe_XUcAABT41?format=jpg&name=360x360"
                    )
                    db.execute(
                        "UPDATE luckydogs SET (LuckyDogs, LastUpdated) = (?, ?) WHERE UserID = ?",
                        LuckyDogs[0][0] + 1,
                        datetime.utcnow(),
                        ctx.author.id,
                    )
                    await ctx.send(embed=embed)

                elif random == 51:
                    embed = Embed(
                        title="Lucky Dog Picture!",
                        description="There is a 1 in 50 chance of getting this picture!",
                        colour=Colour.gold(),
                    )
                    embed.set_footer(
                        text=f"{ctx.author} got this lucky dog picture!",
                        icon_url=ctx.author.avatar_url,
                    )
                    embed.set_image(url="https://i.imgur.com/pzqRLdi.jpg")
                    db.execute(
                        "UPDATE luckydogs SET (LuckyDogs, LastUpdated) = (?, ?) WHERE UserID = ?",
                        LuckyDogs[0][0] + 1,
                        datetime.utcnow(),
                        ctx.author.id,
                    )
                    await ctx.send(embed=embed)

                elif random == 52:
                    embed = Embed(
                        title="Lucky Dog Picture!",
                        description="This is [Weest](https://twitter.com/weesterner)'s dog Kevin!",
                        colour=Colour.gold(),
                    )
                    embed.set_footer(
                        text=f"{ctx.author} got this lucky dog picture! | There is a 1 in 50 chance of getting this picture!",
                        icon_url=ctx.author.avatar_url,
                    )
                    embed.set_image(url="https://i.imgur.com/guF2Y3z.png")
                    db.execute(
                        "UPDATE luckydogs SET (LuckyDogs, LastUpdated) = (?, ?) WHERE UserID = ?",
                        LuckyDogs[0][0] + 1,
                        datetime.utcnow(),
                        ctx.author.id,
                    )
                    await ctx.send(embed=embed)

                elif random == 53:
                    embed = Embed(
                        title="Lucky Dog Picture!",
                        description="This is [@KittyKay000](https://twitter.com/kittykay000)'s concept drawing of Doob!",
                        colour=Colour.gold(),
                    )
                    embed.set_footer(
                        text=f"{ctx.author} got this lucky dog picture! | There is a 1 in 50 chance of getting this picture!",
                        icon_url=ctx.author.avatar_url,
                    )
                    embed.set_image(url="https://i.imgur.com/KFOR8YJ.jpeg")
                    db.execute(
                        "UPDATE luckydogs SET (LuckyDogs, LastUpdated) = (?, ?) WHERE UserID = ?",
                        LuckyDogs[0][0] + 1,
                        datetime.utcnow(),
                        ctx.author.id,
                    )
                    await ctx.send(embed=embed)

            else:
                # If they aren't a Patron, it calls the function below.
                await self.lucky_dogs(ctx)

        else:
            # If they aren't in the support server, it calls the function below.
            await self.lucky_dogs(ctx)

    async def lucky_dogs(self, ctx):
        # Rolls a number for the Lucky Dogs
        random = randint(1, 503)
        # Rolls a number for the "Patreon Ad", which is just a small ad at the top of the embed telling them that they can get
        # a higher chance of getting a Lucky Dog by subscribing to the Patreon.
        patreon_ad = randint(1, 4)

        LuckyDogs = db.records(
            "SELECT LuckyDogs FROM luckydogs WHERE UserID = ?", ctx.author.id
        )

        # URL for the API
        URL = "https://dog.ceo/api/breeds/image/random"

        if random != 100 and random != 101 and random != 102:
            # This is for the "Patreon Ad" at the top of d!dog you get times.
            if patreon_ad != 1:
                async with request("GET", URL, headers={}) as response:
                    if response.status == 200:
                        data = await response.json()
                        embed = Embed(title="Dog Picture!", colour=ctx.author.colour)
                        embed.set_image(url=data["message"])
                        await ctx.send(embed=embed)
            elif patreon_ad == 1:
                async with request("GET", URL, headers={}) as response:
                    if response.status == 200:
                        data = await response.json()
                        embed = Embed(title="Dog Picture!", colour=ctx.author.colour)
                        embed.set_author(
                            name="Get a higher chance of getting a Lucky Dog by subscribing to our Patreon",
                            icon_url="https://i.imgur.com/OosmBb4.png",
                            url="https://patreon.com/doobdev",
                        )
                        embed.set_image(url=data["message"])
                        await ctx.send(embed=embed)

        # If they get a lucky dog, run this instead of ^.
        elif random == 100:
            embed = Embed(
                title="Lucky Dog Picture!",
                description="This is [Liquid Mendo](https://twitter.com/mendo)'s dog Koda!",
                colour=Colour.gold(),
            )
            embed.set_footer(
                text=f"{ctx.author} got this lucky dog picture! | There is a 1 in 1000 chance of getting this picture!",
                icon_url=ctx.author.avatar_url,
            )
            embed.set_image(
                url="https://pbs.twimg.com/media/EgXfe_XUcAABT41?format=jpg&name=360x360"
            )
            db.execute(
                "UPDATE luckydogs SET (LuckyDogs, LastUpdated) = (?, ?) WHERE UserID = ?",
                LuckyDogs[0][0] + 1,
                datetime.utcnow(),
                ctx.author.id,
            )
            await ctx.send(embed=embed)

        elif random == 101:
            embed = Embed(
                title="Lucky Dog Picture!",
                description="There is a 1 in 1000 chance of getting this picture!",
                colour=Colour.gold(),
            )
            embed.set_footer(
                text=f"{ctx.author} got this lucky dog picture!",
                icon_url=ctx.author.avatar_url,
            )
            embed.set_image(url="https://i.imgur.com/pzqRLdi.jpg")
            db.execute(
                "UPDATE luckydogs SET (LuckyDogs, LastUpdated) = (?, ?) WHERE UserID = ?",
                LuckyDogs[0][0] + 1,
                datetime.utcnow(),
                ctx.author.id,
            )
            await ctx.send(embed=embed)

        elif random == 102:
            embed = Embed(
                title="Lucky Dog Picture!",
                description="This is [Weest](https://twitter.com/weesterner)'s dog Kevin!",
                colour=Colour.gold(),
            )
            embed.set_footer(
                text=f"{ctx.author} got this lucky dog picture! | There is a 1 in 1000 chance of getting this picture!",
                icon_url=ctx.author.avatar_url,
            )
            embed.set_image(url="https://i.imgur.com/guF2Y3z.png")
            db.execute(
                "UPDATE luckydogs SET (LuckyDogs, LastUpdated) = (?, ?) WHERE UserID = ?",
                LuckyDogs[0][0] + 1,
                datetime.utcnow(),
                ctx.author.id,
            )
            await ctx.send(embed=embed)

        elif random == 103:
            embed = Embed(
                title="Lucky Dog Picture!",
                description="This is [@KittyKay000](https://twitter.com/kittykay000)'s concept drawing of Doob!",
                colour=Colour.gold(),
            )
            embed.set_footer(
                text=f"{ctx.author} got this lucky dog picture! | There is a 1 in 1000 chance of getting this picture!",
                icon_url=ctx.author.avatar_url,
            )
            embed.set_image(url="https://i.imgur.com/KFOR8YJ.jpeg")
            db.execute(
                "UPDATE luckydogs SET (LuckyDogs, LastUpdated) = (?, ?) WHERE UserID = ?",
                LuckyDogs[0][0] + 1,
                datetime.utcnow(),
                ctx.author.id,
            )
            await ctx.send(embed=embed)

    @command(name="nukeserver", brief="We do a little trolling", hidden=True)
    @cooldown(1, 5, BucketType.guild)
    async def nuke_server_trollage_command(self, ctx):
        msg = await ctx.send("Nuking Server [------------------]")

        await sleep(1)

        await msg.edit(content="Nuking Server [=-----------------]")
        await sleep(1)

        await msg.edit(content="Nuking Server [==----------------]")
        await sleep(1)

        await msg.edit(content="Nuking Server [===---------------]")
        await sleep(1)

        await msg.edit(content="Nuking Server [====--------------]")
        await sleep(1)

        await msg.edit(content="Nuking Server [=====-------------]")
        await sleep(1)

        await msg.edit(content="Nuking Server [======------------]")
        await sleep(1)

        await msg.edit(content="Nuking Server [=======-----------]")
        await sleep(1)

        await msg.edit(content="Nuking Server [========----------]")
        await sleep(1)

        await msg.edit(content="Nuking Server [=========---------]")
        await sleep(1)

        await msg.edit(content="Nuking Server [==========--------]")
        await sleep(1)

        await msg.edit(content="Nuking Server [===========-------]")
        await sleep(1)

        await msg.edit(content="Nuking Server [============------]")
        await sleep(1)

        await msg.edit(content="Nuking Server [=============-----]")
        await sleep(1)

        await msg.edit(content="Nuking Server [==============----]")
        await sleep(1)

        await msg.edit(content="Nuking Server [===============---]")
        await sleep(1)

        await msg.edit(content="Nuking Server [================--]")
        await sleep(1)

        await msg.edit(content="Nuking Server [=================-]")
        await sleep(1)

        await msg.edit(content="Nuking Server [==================]")
        await sleep(1)

        await msg.edit(content="trolololol")

    @command(
        name="notanimposter",
        aliases=["nai", "amonguscrew", "crewmate"],
        brief="Shows a user as not the imposter!",
    )
    @cooldown(1, 4, BucketType.user)
    async def not_an_imposter(self, ctx, *, target: Optional[str]):
        """Among Us Command - Shows a user as `not the imposter`\nI SWEAR I SAW HIM VENT! He wasn't an imposter..."""
        target = target or ctx.author

        # Checks if the target is an "@everyone" or "@here" ping, so Doob doesn't ping the entire server.
        if target == "@everyone" or target == "@here":
            await ctx.reply("nope, no ping pong here.")

        else:
            await ctx.reply(
                f". 　　　。　　　　•　 　ﾟ　　。 　　.\n　　　.　　　 　　.　　　　　。　　 。　. 　\n\n.　　 。　　　　　 ඞ 。 . 　　 • 　　　　•\n\n　　ﾟ　　 {target} was not An Impostor.　 。　.\n\n　　'　　　 1 Impostor remain 　 　　。\n\n　　ﾟ　　　.　　　. ,　　　　.　 ."
            )

    @command(
        name="animposter",
        aliases=["ai", "amongusimposter", "imposter"],
        brief="Shows a user as the imposter!",
    )
    @cooldown(1, 4, BucketType.user)
    async def an_imposter(self, ctx, *, target: Optional[str]):
        """Among Us Command - Shows a user as `the imposter`\nI SWEAR I SAW HIM VENT! He was an imposter. I knew it!!!"""
        target = target or ctx.author

        if target == "@everyone" or target == "@here":
            await ctx.reply("nope, no ping pong here.")

        else:
            await ctx.reply(
                f". 　　　。　　　　•　 　ﾟ　　。 　　.\n　　　.　　　 　　.　　　　　。　　 。　. 　\n\n.　　 。　　　　　 ඞ 。 . 　　 • 　　　　•\n\n　　ﾟ　　 {target} was An Impostor.　 。　.\n\n　　'　　　 0 Impostors remain 　 　　。\n\n　　ﾟ　　　.　　　. ,　　　　.　 ."
            )

    async def valroll_func(self, ctx):
        characters = (
            "Viper",
            "Sova",
            "Sage",
            "Reyna",
            "Raze",
            "Phoenix",
            "Omen",
            "Jett",
            "Cypher",
            "Brimstone",
            "Breach",
            "Killjoy",
            "Skye",
            "Yoru",
            "Astra",
        )

        char = choice((characters))

        print(char)

        embed = Embed(
            title=f"Play: {char}", description="Enjoy!", colour=ctx.author.colour
        )

        if char == "Brimstone":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/3/37/Brimstone_artwork.png/revision/latest/scale-to-width-down/587?cb=20200602020239"
            )

        elif char == "Viper":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/9/91/Viper_artwork.png/revision/latest/scale-to-width-down/587?cb=20200602020322"
            )

        elif char == "Omen":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/0/06/Omen_artwork.png/revision/latest/scale-to-width-down/587?cb=20200602020233"
            )

        elif char == "Killjoy":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/8/8c/Killjoy.png/revision/latest/scale-to-width-down/587?cb=20200729134445"
            )

        elif char == "Cypher":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/b/bb/Cypher_artwork.png/revision/latest/scale-to-width-down/587?cb=20200602020329"
            )

        elif char == "Sova":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/6/61/Sova_artwork.png/revision/latest/scale-to-width-down/587?cb=20200602020314"
            )

        elif char == "Sage":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/1/1e/Sage_artwork.png/revision/latest/scale-to-width-down/587?cb=20200602020306"
            )

        elif char == "Phoenix":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/f/fa/Phoenix_artwork.png/revision/latest/scale-to-width-down/652?cb=20200602020246"
            )

        elif char == "Jett":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/7/79/Jett_artwork.png/revision/latest/scale-to-width-down/587?cb=20200602020209"
            )

        elif char == "Reyna":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/4/41/Reyna_artwork.png/revision/latest/scale-to-width-down/587?cb=20200602020340"
            )

        elif char == "Raze":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/c/c4/Raze_artwork.png/revision/latest/scale-to-width-down/587?cb=20200602020217"
            )

        elif char == "Breach":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/5/5c/Breach_artwork.png/revision/latest/scale-to-width-down/587?cb=20200602020225"
            )

        elif char == "Skye":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/b/b9/Skye_Keyart_final.png/revision/latest/scale-to-width-down/587?cb=20201013182515"
            )

        elif char == "Yoru":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/a/a1/Yoru2.png/revision/latest/scale-to-width-down/587?cb=20210112180407"
            )

        elif char == "Astra":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/8/8a/Astra_artwork.png/revision/latest/scale-to-width-down/326?cb=20210302170140"
            )

        await ctx.reply(embed=embed)

    @group(name="valroll", brief="Roll a random VALORANT character.")
    @cooldown(1, 2, BucketType.user)
    async def valroll(self, ctx):
        """Get a random VALORANT character to play!"""
        if ctx.invoked_subcommand is None:
            await self.valroll_func(ctx)

    @valroll.command(name="-duelists", aliases=["-duel"])
    async def valroll_duelists_command(self, ctx):
        characters = (
            "Reyna",
            "Raze",
            "Phoenix",
            "Jett",
            "Yoru",
        )

        char = choice((characters))

        print(char)

        embed = Embed(
            title=f"Play: {char}", description="Enjoy!", colour=ctx.author.colour
        )

        if char == "Phoenix":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/f/fa/Phoenix_artwork.png/revision/latest/scale-to-width-down/652?cb=20200602020246"
            )

        elif char == "Jett":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/7/79/Jett_artwork.png/revision/latest/scale-to-width-down/587?cb=20200602020209"
            )

        elif char == "Reyna":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/4/41/Reyna_artwork.png/revision/latest/scale-to-width-down/587?cb=20200602020340"
            )

        elif char == "Raze":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/c/c4/Raze_artwork.png/revision/latest/scale-to-width-down/587?cb=20200602020217"
            )

        elif char == "Yoru":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/a/a1/Yoru2.png/revision/latest/scale-to-width-down/587?cb=20210112180407"
            )

        await ctx.reply(embed=embed)

    @valroll.command(name="-sentinels", aliases=["-sen", "-sentinel"])
    async def valroll_sentinels_command(self, ctx):
        characters = (
            "Sage",
            "Cypher",
            "Killjoy",
        )

        char = choice((characters))

        print(char)

        embed = Embed(
            title=f"Play: {char}", description="Enjoy!", colour=ctx.author.colour
        )

        if char == "Sage":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/1/1e/Sage_artwork.png/revision/latest/scale-to-width-down/587?cb=20200602020306"
            )

        elif char == "Cypher":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/b/bb/Cypher_artwork.png/revision/latest/scale-to-width-down/587?cb=20200602020329"
            )

        elif char == "Killjoy":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/8/8c/Killjoy.png/revision/latest/scale-to-width-down/587?cb=20200729134445"
            )

        await ctx.reply(embed=embed)

    @valroll.command(name="-initiators", aliases=["-init", "-initiator"])
    async def valroll_initiators_command(self, ctx):
        characters = (
            "Breach",
            "Sova",
            "Skye",
        )

        char = choice((characters))

        print(char)

        embed = Embed(
            title=f"Play: {char}", description="Enjoy!", colour=ctx.author.colour
        )

        if char == "Breach":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/5/5c/Breach_artwork.png/revision/latest/scale-to-width-down/587?cb=20200602020225"
            )

        elif char == "Sova":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/6/61/Sova_artwork.png/revision/latest/scale-to-width-down/587?cb=20200602020314"
            )

        elif char == "Skye":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/b/b9/Skye_Keyart_final.png/revision/latest/scale-to-width-down/587?cb=20201013182515"
            )

        await ctx.reply(embed=embed)

    @valroll.command(name="-controllers", aliases=["-ctrl", "-controller"])
    async def valroll_controllers_command(self, ctx):
        characters = (
            "Omen",
            "Brimstone",
            "Viper",
            "Astra",
        )

        char = choice((characters))

        print(char)

        embed = Embed(
            title=f"Play: {char}", description="Enjoy!", colour=ctx.author.colour
        )

        if char == "Omen":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/0/06/Omen_artwork.png/revision/latest/scale-to-width-down/587?cb=20200602020233"
            )

        elif char == "Brimstone":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/3/37/Brimstone_artwork.png/revision/latest/scale-to-width-down/587?cb=20200602020239"
            )

        elif char == "Viper":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/9/91/Viper_artwork.png/revision/latest/scale-to-width-down/587?cb=20200602020322"
            )

        elif char == "Astra":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/8/8a/Astra_artwork.png/revision/latest/scale-to-width-down/326?cb=20210302170140"
            )

        await ctx.reply(embed=embed)

    @command(name="owoify", aliases=["owo"], brief="'Owoify' your text.")
    async def owoify_command(self, ctx, *, text: str):
        """<:4Weird:799869851190558751> 🤚🛑 STOP IT WEEBS"""
        owo_text = owoifactor.owoify(text)

        await ctx.reply(f"{owo_text}")

    @command(
        name="owroll",
        aliases=["overwatchroll"],
        brief="Roll a random Overwatch character.",
    )
    @cooldown(1, 3, BucketType.user)
    async def overwatch_roll_command(self, ctx):
        """Get a random Overwatch character to play!"""
        characters = (
            "D.va",
            "Orisa",
            "Reinhardt",
            "Roadhog",
            "Sigma",
            "Winston",
            "Wrecking Ball",
            "Zarya",
            "Ashe",
            "Bastion",
            "Doobfist",
            "Echo",
            "Genji",
            "Hanzo",
            "Junkrat",
            "McCree",
            "Mei",
            "Pharah",
            "Reaper",
            "Soldier: 76",
            "Sombra",
            "Symmetra",
            "Torbjörn",
            "Tracer",
            "Widowmaker",
            "Ana",
            "Baptiste",
            "Brigitte",
            "Lúcio",
            "Mercy",
            "Moira",
            "Zenyatta",
        )

        char = choice((characters))

        print(char)

        embed = Embed(
            title=f"Play: {char}", description="Enjoy!", colour=ctx.author.colour
        )

        if char == "D.va":
            embed.set_image(
                url="https://static.wikia.nocookie.net/overwatch/images/d/dc/Dva_portrait.png/revision/latest/scale-to-width-down/786?cb=20160429040128"
            )

        elif char == "Orisa":
            embed.set_image(
                url="https://static.wikia.nocookie.net/overwatch/images/f/f9/Orisa_portrait.png/revision/latest/scale-to-width-down/795?cb=20170323183330"
            )

        elif char == "Reinhardt":
            embed.set_image(
                url="https://static.wikia.nocookie.net/overwatch/images/a/a2/Reinhardt-ow2.png/revision/latest/scale-to-width-down/1000?cb=20201021030948"
            )

        elif char == "Roadhog":
            embed.set_image(
                url="https://static.wikia.nocookie.net/overwatch/images/1/15/Roadhog_portrait_m.png/revision/latest/scale-to-width-down/1000?cb=20160429040723"
            )

        elif char == "Sigma":
            embed.set_image(
                url="https://static.wikia.nocookie.net/overwatch/images/6/6a/Sigma_Portrait.png/revision/latest/scale-to-width-down/621?cb=20200326150607"
            )

        elif char == "Winston":
            embed.set_image(
                url="https://static.wikia.nocookie.net/overwatch/images/1/1f/Winston-ow2.png/revision/latest/scale-to-width-down/852?cb=20201122033102"
            )

        elif char == "Wrecking Ball":
            embed.set_image(
                url="https://static.wikia.nocookie.net/overwatch/images/8/83/WreckingBall_portrait.png/revision/latest?cb=20190114232714"
            )

        elif char == "Zarya":
            embed.set_image(
                url="https://static.wikia.nocookie.net/overwatch/images/d/d1/Zarya_portrait.png/revision/latest/scale-to-width-down/725?cb=20160429041121"
            )

        elif char == "Ashe":
            embed.set_image(
                url="https://static.wikia.nocookie.net/overwatch/images/c/c1/Ashe_portrait2.png/revision/latest/scale-to-width-down/878?cb=20181106125518"
            )

        elif char == "Bastion":
            embed.set_image(
                url="https://static.wikia.nocookie.net/overwatch/images/6/6a/Bastion_portrait.png/revision/latest/scale-to-width-down/932?cb=20160429042023"
            )

        elif char == "Doomfist":
            embed.set_image(
                url="https://static.wikia.nocookie.net/overwatch/images/0/0e/Doomfist_portrait.png/revision/latest/scale-to-width-down/699?cb=20170807035611"
            )

        elif char == "Echo":
            embed.set_image(
                url="https://static.wikia.nocookie.net/overwatch/images/5/53/Echo_portrait.png/revision/latest/scale-to-width-down/321?cb=20200319191425"
            )

        elif char == "Genji":
            embed.set_image(
                url="https://static.wikia.nocookie.net/overwatch/images/2/23/Genji-ow2.png/revision/latest/scale-to-width-down/521?cb=20201122032955"
            )

        elif char == "Hanzo":
            embed.set_image(
                url="https://static.wikia.nocookie.net/overwatch/images/c/c2/Hanzo_portrait.png/revision/latest/scale-to-width-down/579?cb=20160429042113"
            )

        elif char == "Junkrat":
            embed.set_image(
                url="https://static.wikia.nocookie.net/overwatch/images/5/53/Junkrat_portrait.png/revision/latest/scale-to-width-down/545?cb=20160429040823"
            )

        elif char == "McCree":
            embed.set_image(
                url="https://static.wikia.nocookie.net/overwatch/images/f/f3/Mccree_portrait.png/revision/latest/scale-to-width-down/748?cb=20160429041214"
            )

        elif char == "Mei":
            embed.set_image(
                url="https://static.wikia.nocookie.net/overwatch/images/3/33/Mei-ow2.png/revision/latest/scale-to-width-down/595?cb=20201122033029"
            )

        elif char == "Pharah":
            embed.set_image(
                url="https://static.wikia.nocookie.net/overwatch/images/f/fe/Pharah_portrait.png/revision/latest/scale-to-width-down/725?cb=20160429041650"
            )

        elif char == "Reaper":
            embed.set_image(
                url="https://static.wikia.nocookie.net/overwatch/images/e/ee/Reaper_portrait.png/revision/latest/scale-to-width-down/721?cb=20160429041404"
            )

        elif char == "Soldier: 76":
            embed.set_image(
                url="https://static.wikia.nocookie.net/overwatch/images/c/c3/Soldier76_portrait.png/revision/latest/scale-to-width-down/653?cb=20160429041023"
            )

        elif char == "Sombra":
            embed.set_image(
                url="https://static.wikia.nocookie.net/overwatch/images/f/fc/Sombra_portrait.png/revision/latest/scale-to-width-down/518?cb=20170105140023"
            )

        elif char == "Symmetra":
            embed.set_image(
                url="https://static.wikia.nocookie.net/overwatch/images/e/eb/Symmetra_portrait.png/revision/latest/scale-to-width-down/546?cb=20160429041836"
            )

        elif char == "Torbjörn":
            embed.set_image(
                url="https://static.wikia.nocookie.net/overwatch/images/e/e5/Torbjorn_portrait.png/revision/latest/scale-to-width-down/819?cb=20160429041926"
            )

        elif char == "Tracer":
            embed.set_image(
                url="https://static.wikia.nocookie.net/overwatch/images/0/07/Tracer-ow2.png/revision/latest/scale-to-width-down/424?cb=20201122033046"
            )

        elif char == "Widowmaker":
            embed.set_image(
                url="https://static.wikia.nocookie.net/overwatch/images/1/1e/Widow.png/revision/latest/scale-to-width-down/1000?cb=20201211185156"
            )

        elif char == "Ana":
            embed.set_image(
                url="https://static.wikia.nocookie.net/overwatch/images/0/0b/Ana_portrait2.png/revision/latest/scale-to-width-down/1000?cb=20181108050042"
            )

        elif char == "Baptiste":
            embed.set_image(
                url="https://static.wikia.nocookie.net/overwatch/images/1/1c/Baptiste_Portrait.png/revision/latest/scale-to-width-down/502?cb=20200326145408"
            )

        elif char == "Brigitte":
            embed.set_image(
                url="https://static.wikia.nocookie.net/overwatch/images/7/7b/Brigitte_portrait.png/revision/latest/scale-to-width-down/750?cb=20190114232133"
            )

        elif char == "Lúcio":
            embed.set_image(
                url="https://static.wikia.nocookie.net/overwatch/images/4/44/Lucio-ow2.png/revision/latest/scale-to-width-down/455?cb=20201122033010"
            )

        elif char == "Mercy":
            embed.set_image(
                url="https://static.wikia.nocookie.net/overwatch/images/7/75/Mercy-ow2.png/revision/latest/scale-to-width-down/505?cb=20201122032817"
            )

        elif char == "Moira":
            embed.set_image(
                url="https://static.wikia.nocookie.net/overwatch/images/a/a2/Moira_portrait0.png/revision/latest/scale-to-width-down/747?cb=20181108054744"
            )

        elif char == "Zenyatta":
            embed.set_image(
                url="https://static.wikia.nocookie.net/overwatch/images/f/f5/Zenyatta_portrait.png/revision/latest/scale-to-width-down/846?cb=20160429042336"
            )

        await ctx.reply(embed=embed)

    @command(name="coinflip", aliases=["cf"], brief="Flip a coin")
    async def coin_flip_command(self, ctx):
        if random() > 0.001:
            await ctx.reply(choice(("Heads!", "Tails!")))
        else:
            await ctx.reply("The coin landed on its side...")

    @command(name="coinfliptimes", aliases=["cft"], brief="Flip a coin multiple times")
    async def coin_flip_times_command(self, ctx, num: int):
        heads = 0
        tails = 0

        if num <= 1000:
            num = num
            num_limit = False
        else:
            num = 1000
            num_limit = True

        for x in range(0, num):
            coinflip = choice(("Heads", "Tails"))
            if coinflip == "Heads":
                heads += 1
            elif coinflip == "Tails":
                tails += 1

        embed = Embed(
            title="Coinflip Results:",
            description=f"Tails: {str(tails)}\nHeads: {str(heads)}",
            colour=ctx.author.color,
        )

        if tails > heads:
            embed.set_footer(
                text=f"Tails won by {tails-heads}!", icon_url=ctx.author.avatar_url
            )

        elif tails < heads:
            embed.set_footer(
                text=f"Heads won by {heads-tails}!", icon_url=ctx.author.avatar_url
            )

        else:
            embed.set_footer(text="TIE!", icon_url=ctx.author.avatar_url)

        if num_limit:
            embed.set_footer(
                text="The maximum number is 1000, your number was too big.",
                icon_url=ctx.author.avatar_url,
            )

        await ctx.reply(embed=embed)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")


def setup(bot):
    bot.add_cog(Fun(bot))
