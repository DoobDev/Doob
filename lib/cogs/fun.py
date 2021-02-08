from random import choice, randint
from typing import Optional
from aiohttp import request
from datetime import datetime

from discord import Member, Embed, Colour
from discord.ext.commands import Cog, command, cooldown, BucketType
from discord.utils import get

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
                await ctx.reply(message)
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

    async def lucky_dogs(self, ctx):
        # Rolls a number for the Lucky Dogs
        random = randint(1, 503)
        # Rolls a number for the "Patreon Ad", which is just a small ad at the top of the embed telling them that they can get
        # a higher chance of getting a Lucky Dog by subscribing to the Patreon.
        patreon_ad = randint(1, 4)

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
                        await ctx.reply(embed=embed)
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
                        await ctx.reply(embed=embed)

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
            await ctx.reply(embed=embed)

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
            await ctx.reply(embed=embed)

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
            await ctx.reply(embed=embed)

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
            await ctx.reply(embed=embed)

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

    @command(name="valroll", brief="Roll a random VALORANT character.")
    @cooldown(1, 2, BucketType.user)
    async def roll_valorant_command(self, ctx):
        """Get a random VALORANT character to play!"""
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

        if char == "Viper":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/9/91/Viper_artwork.png/revision/latest/scale-to-width-down/587?cb=20200602020322"
            )

        if char == "Omen":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/0/06/Omen_artwork.png/revision/latest/scale-to-width-down/587?cb=20200602020233"
            )

        if char == "Killjoy":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/8/8c/Killjoy.png/revision/latest/scale-to-width-down/587?cb=20200729134445"
            )

        if char == "Cypher":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/b/bb/Cypher_artwork.png/revision/latest/scale-to-width-down/587?cb=20200602020329"
            )

        if char == "Sova":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/6/61/Sova_artwork.png/revision/latest/scale-to-width-down/587?cb=20200602020314"
            )

        if char == "Sage":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/1/1e/Sage_artwork.png/revision/latest/scale-to-width-down/587?cb=20200602020306"
            )

        if char == "Phoenix":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/1/1e/Sage_artwork.png/revision/latest/scale-to-width-down/587?cb=20200602020306"
            )

        if char == "Jett":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/7/79/Jett_artwork.png/revision/latest/scale-to-width-down/587?cb=20200602020209"
            )

        if char == "Reyna":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/4/41/Reyna_artwork.png/revision/latest/scale-to-width-down/587?cb=20200602020340"
            )

        if char == "Raze":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/c/c4/Raze_artwork.png/revision/latest/scale-to-width-down/587?cb=20200602020217"
            )

        if char == "Breach":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/5/5c/Breach_artwork.png/revision/latest/scale-to-width-down/587?cb=20200602020225"
            )

        if char == "Skye":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/b/b9/Skye_Keyart_final.png/revision/latest/scale-to-width-down/587?cb=20201013182515"
            )

        if char == "Yoru":
            embed.set_image(
                url="https://static.wikia.nocookie.net/valorant/images/a/a1/Yoru2.png/revision/latest/scale-to-width-down/587?cb=20210112180407"
            )

        await ctx.reply(embed=embed)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")


def setup(bot):
    bot.add_cog(Fun(bot))
