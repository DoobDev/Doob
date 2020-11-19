from random import choice, randint
from typing import Optional
from aiohttp import request
from datetime import datetime

from discord import Member, Embed, Colour
from discord.ext.commands import Cog, command, cooldown, BucketType
from discord.utils import get

from ..db import db # pylint: disable=relative-beyond-top-level

class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="hello", aliases=["hi"], brief="Say Hi to Doob!")
    async def say_hello(self, ctx):
        """Say Hi to Doob!"""
        # Chooses Hello, Hi, or Hey at random, to say Hi to the user.
        await ctx.send(f"{choice(('Hello', 'Hi', 'Hey'))} {ctx.author.mention}!")

    @command(name="dice", aliases=["roll", "rolldice"], brief="Roll some dice!")
    @cooldown(1, 10, BucketType.user)
    async def roll_dice(self, ctx, die_string: str):
        """Role some dice, (number)d(number) syntax."""
        dice, value = (int(term) for term in die_string.split("d"))

        # If the dice is less or equal to 40, then run the command
        if dice <= 40:
            rolls = [randint(1, value) for i in range(dice)]

            await ctx.send(" + ".join([str(r) for r in  rolls]) + f" = {sum(rolls)}")
        
        # If the dice number is too high, we don't run the command
        # This is because higher then 40 dice can lead to errors regarding message length.
        else:
            await ctx.send("Please roll a lower number of dice.", delete_after=10)

    @command(name="echo", aliases=["say"], brief="Make Doob say something!")
    @cooldown(1, 10, BucketType.user)
    async def echo_message(self, ctx, *, message):
        """Make Doob say a message! | `Patreon Only`"""
        homeGuild = self.bot.get_guild(702352937980133386)         # Support Server ID.
        patreonRole = get(homeGuild.roles, id=757041749716893739)  # Patreon role ID.

        member = []

        # Checks if a user is a Patreon member.
        for pledger in homeGuild.members:
            if pledger == ctx.author:
                member = pledger

        if ctx.author in homeGuild.members:
            if patreonRole in member.roles:
                # If they are, run the command.
                    await ctx.send(message)
                    print(f"{ctx.author.name} used the Echo command and said {message}")

            # This else is for if they are in the server, but not a Patron
            else:
                await ctx.send("You are not a Patron to Doob, subscribe to any of the tiers at <https://patreon.com/doobdev> to gain access to this command.")

        # This else is for if they aren't in the server, and are not a Patreon (you can only get Patron benefits by joining the Support Server)
        else:
            await ctx.send("You are not a Patron to Doob, subscribe to any of the tiers at <https://patreon.com/doobdev> to gain access to this command.")

    @command(name="fact", aliases=["dogfact", "facts"], brief="Learn a random fact about dogs!")
    @cooldown(3, 10, BucketType.user)
    async def dog_fact(self, ctx):
        """Get a wacky dog fact"""
        # URL of the API
        URL = "https://some-random-api.ml/facts/dog"

        # GETs a json response from URL, puts the fact into an embed, then sends it to the user.
        async with request("GET", URL, headers={}) as response:
            if response.status == 200:
                data = await response.json()                # Right here is where it gets the data from the json response.
                embed = Embed(title="Dog Fact!", description=data["fact"], colour=ctx.author.colour)
                embed.set_footer(text=f"{ctx.author} requested this fact!", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            else:
                # if the API responds with a status not being "200" (200=Working just fine), sends out an error message to the user with the status number.
                await ctx.send(f"Dog fact API sent a {response.status} status.")

    @command(name="luckydog", aliases=["ldog"], brief="Get an instant Lucky Dog!")
    @cooldown(2, 5, BucketType.user)
    async def lucky_dog_image(self, ctx, *, dog: Optional[str]):
        """Shows the lucky dogs possible!\nIsn't eligable for the Nitro Giveaways\n`Patreon` permission required"""
        homeGuild = self.bot.get_guild(702352937980133386)         # Support Server ID.
        patreonRole = get(homeGuild.roles, id=757041749716893739)  # Patreon role ID.

        member = []

        # Checks if someone is a Patron
        for pledger in homeGuild.members:
            if pledger == ctx.author:
                member = pledger

        # If they are, let them run the command
        if ctx.author in homeGuild.members:
            if patreonRole in member.roles:
                if dog == "1":
                    embed = Embed(title="Lucky Dog Picture!", description="This is [Liquid Mendo](https://twitter.com/Mendo)'s dog Koda!", colour=Colour.gold())
                    embed.set_footer(text=f"{ctx.author} got this lucky dog picture!", icon_url=ctx.author.avatar_url)
                    embed.set_image(url="https://pbs.twimg.com/media/EgXfe_XUcAABT41?format=jpg&name=360x360")
                    await ctx.send(embed=embed)

                elif dog == "2":
                    embed = Embed(title="Lucky Dog Picture!", description="You selected the old `GAMING` server PFP!", colour=Colour.gold())
                    embed.set_footer(text=f"Thanks for supporting Doob, {ctx.author.name}!", icon_url=ctx.author.avatar_url)
                    embed.set_image(url="https://i.imgur.com/pzqRLdi.jpg")
                    await ctx.send(embed=embed)

                elif dog == "3":
                    embed = Embed(title="Lucky Dog Picture!", description="This is [Weest](https://twitter.com/weesterner)'s dog Kevin!", colour=Colour.gold())
                    embed.set_footer(text=f"Thanks for supporting Doob, {ctx.author.name}!", icon_url=ctx.author.avatar_url)
                    embed.set_image(url="https://i.imgur.com/guF2Y3z.png")
                    await ctx.send(embed=embed)
                
                elif dog == "4":
                    embed = Embed(title="Lucky Dog Picture!", description="This is [@KittyKay000](https://twitter.com/kittykay000)'s concept drawing of Doob!", colour=Colour.gold())
                    embed.set_footer(text=f"Thanks for supporting Doob, {ctx.author.name}!", icon_url=ctx.author.avatar_url)
                    embed.set_image(url="https://i.imgur.com/KFOR8YJ.jpeg")
                    await ctx.send(embed=embed)

                else:
                    embed = Embed(title="Lucky Dogs Possible:", description="1 = [Liquid Mendo](https://twitter.com/mendo)'s dog Koda\n2 = Old `GAMING` server PFP\n3 = [Weest](https://twitter.com/weesterner)'s dog Kevin\n4 = [@KittyKay000](https://twitter.com/kittykay000)'s concept drawing for Doob!", colour=ctx.author.colour)
                    embed.set_footer(text=f"Thanks for supporting Doob, {ctx.author.name}!", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)

# Refer to line 59 and 63 for reasoning on the bottom 2 elses.
            else:
                await ctx.send("This is a Patreon (<https://patreon.com/doobdev>) only command.")
        
        else:
            await ctx.send("This is a Patreon (<https://patreon.com/doobdev>) only command.")

    @command(name="luckydogs", aliases=["dogscaught", "ldc", "ld", "checkdogs", "lds"], brief="Check how many Lucky Dogs you have gotten!")
    @cooldown(2, 5, BucketType.user)
    async def check_lucky_dogs(self, ctx, *, target: Optional[Member]):
        """Check how many Lucky dogs you have gotten in the last month!"""
        target = target or ctx.author

        # Pulls from the database how many luckydogs a user has.
        LuckyDogs = db.records("SELECT LuckyDogs FROM luckydogs WHERE UserID = ?", target.id)
        
        # Gives how many lucky dogs a user has.
        embed = Embed(title=f"{target.name} has gotten:", description=f"{str(LuckyDogs[0][0])} Lucky Dog(s) this month.", colour=target.colour)
        embed.set_footer(text=f"{ctx.author.name} requested this. | Doob", icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=target.avatar_url)
        await ctx.send(embed=embed)

    @command(name="dog", aliases=["dogimage"], brief="See a random picture of a dog!")
    @cooldown(2, 5, BucketType.user)
    async def dog_image(self, ctx):
        """So this is what you came for...\nGives you a random picture of a dog!"""
        LuckyDogs = db.records("SELECT LuckyDogs FROM luckydogs WHERE UserID = ?", ctx.author.id)

        # Support Server ID/Patreon Role ID
        homeGuild = self.bot.get_guild(702352937980133386)
        patreonRole = get(homeGuild.roles, id=757041749716893739)
        
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
                random = randint(1,53)

                # If the user doesn't get a lucky dog roll, then contact the API and get a picture!
                if random != 50 and random != 51 and random != 52 and random != 53:
                    async with request("GET", URL, headers={}) as response:
                        if response.status == 200:
                            data = await response.json()
                            embed = Embed(title="Dog Picture!", colour=ctx.author.colour)
                            #embed.set_footer(text=f"DEBUG: L_DOG: {random}")
                            embed.set_image(url=data["message"])
                            await ctx.send(embed=embed)
                
                # This is the Lucky Dog stuff, if the user rolls one of these numbers, they get a "Lucky Dog", that gives them the special dog
                # and gives them 1 "Lucky Dog" into the DB
                elif random == 50:
                    embed = Embed(title="Lucky Dog Picture!", description="This is [Liquid Mendo](https://twitter.com/Mendo)'s dog Koda!", colour=Colour.gold())
                    embed.set_footer(text=f"{ctx.author} got this lucky dog picture! | There is a 1 in 50 chance of getting this picture!", icon_url=ctx.author.avatar_url)
                    embed.set_image(url="https://pbs.twimg.com/media/EgXfe_XUcAABT41?format=jpg&name=360x360")
                    db.execute("UPDATE luckydogs SET (LuckyDogs, LastUpdated) = (?, ?) WHERE UserID = ?", LuckyDogs[0][0] + 1, datetime.utcnow(), ctx.author.id)
                    await ctx.send(embed=embed)

                elif random == 51:
                    embed = Embed(title="Lucky Dog Picture!", description="There is a 1 in 50 chance of getting this picture!", colour=Colour.gold())
                    embed.set_footer(text=f"{ctx.author} got this lucky dog picture!", icon_url=ctx.author.avatar_url)
                    embed.set_image(url="https://i.imgur.com/pzqRLdi.jpg")
                    db.execute("UPDATE luckydogs SET (LuckyDogs, LastUpdated) = (?, ?) WHERE UserID = ?", LuckyDogs[0][0] + 1, datetime.utcnow(), ctx.author.id)
                    await ctx.send(embed=embed)

                elif random == 52:
                    embed = Embed(title="Lucky Dog Picture!", description="This is [Weest](https://twitter.com/weesterner)'s dog Kevin!", colour=Colour.gold())
                    embed.set_footer(text=f"{ctx.author} got this lucky dog picture! | There is a 1 in 50 chance of getting this picture!", icon_url=ctx.author.avatar_url)
                    embed.set_image(url="https://i.imgur.com/guF2Y3z.png")
                    db.execute("UPDATE luckydogs SET (LuckyDogs, LastUpdated) = (?, ?) WHERE UserID = ?", LuckyDogs[0][0] + 1, datetime.utcnow(), ctx.author.id)
                    await ctx.send(embed=embed)
                
                elif random == 53:
                    embed = Embed(title="Lucky Dog Picture!", description="This is [@KittyKay000](https://twitter.com/kittykay000)'s concept drawing of Doob!", colour=Colour.gold())
                    embed.set_footer(text=f"{ctx.author} got this lucky dog picture! | There is a 1 in 50 chance of getting this picture!", icon_url=ctx.author.avatar_url)
                    embed.set_image(url="https://i.imgur.com/KFOR8YJ.jpeg")
                    db.execute("UPDATE luckydogs SET (LuckyDogs, LastUpdated) = (?, ?) WHERE UserID = ?", LuckyDogs[0][0] + 1, datetime.utcnow(), ctx.author.id)
                    await ctx.send(embed=embed)

            else:
                # If they aren't a Patron, it calls the function below.
                await self.lucky_dogs(ctx)
                
            
        else:
            # If they aren't in the support server, it calls the function below.
            await self.lucky_dogs(ctx)

    async def lucky_dogs(self, ctx):
        # Rolls a number for the Lucky Dogs
        random = randint(1,503)
        # Rolls a number for the "Patreon Ad", which is just a small ad at the top of the embed telling them that they can get
        # a higher chance of getting a Lucky Dog by subscribing to the Patreon.
        patreon_ad = randint(1, 4)

        # URL for the API
        URL = "https://dog.ceo/api/breeds/image/random"

        if random != 100 and random != 101 and random != 102:
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
                        embed=Embed(title="Dog Picture!", colour=ctx.author.colour)
                        embed.set_author(name="Get a higher chance of getting a Lucky Dog by subscribing to our Patreon", icon_url="https://i.imgur.com/OosmBb4.png", url="https://patreon.com/doobdev")
                        embed.set_image(url=data["message"])
                        await ctx.send(embed=embed)

        elif random == 100:
            embed = Embed(title="Lucky Dog Picture!", description="This is [Liquid Mendo](https://twitter.com/mendo)'s dog Koda!", colour=Colour.gold())
            embed.set_footer(text=f"{ctx.author} got this lucky dog picture! | There is a 1 in 1000 chance of getting this picture!", icon_url=ctx.author.avatar_url)
            embed.set_image(url="https://pbs.twimg.com/media/EgXfe_XUcAABT41?format=jpg&name=360x360")
            db.execute("UPDATE luckydogs SET (LuckyDogs, LastUpdated) = (?, ?) WHERE UserID = ?", LuckyDogs[0][0] + 1, datetime.utcnow(), ctx.author.id)
            await ctx.send(embed=embed)

        elif random == 101:
            embed = Embed(title="Lucky Dog Picture!", description="There is a 1 in 1000 chance of getting this picture!", colour=Colour.gold())
            embed.set_footer(text=f"{ctx.author} got this lucky dog picture!", icon_url=ctx.author.avatar_url)
            embed.set_image(url = "https://i.imgur.com/pzqRLdi.jpg")
            db.execute("UPDATE luckydogs SET (LuckyDogs, LastUpdated) = (?, ?) WHERE UserID = ?", LuckyDogs[0][0] + 1, datetime.utcnow(), ctx.author.id)
            await ctx.send(embed=embed)

        elif random == 102:
            embed = Embed(title="Lucky Dog Picture!", description="This is [Weest](https://twitter.com/weesterner)'s dog Kevin!", colour=Colour.gold())
            embed.set_footer(text=f"{ctx.author} got this lucky dog picture! | There is a 1 in 1000 chance of getting this picture!", icon_url=ctx.author.avatar_url)
            embed.set_image(url="https://i.imgur.com/guF2Y3z.png")
            db.execute("UPDATE luckydogs SET (LuckyDogs, LastUpdated) = (?, ?) WHERE UserID = ?", LuckyDogs[0][0] + 1, datetime.utcnow(), ctx.author.id)
            await ctx.send(embed=embed)

        elif random == 103:
            embed = Embed(title="Lucky Dog Picture!", description="This is [@KittyKay000](https://twitter.com/kittykay000)'s concept drawing of Doob!", colour=Colour.gold())
            embed.set_footer(text=f"{ctx.author} got this lucky dog picture! | There is a 1 in 1000 chance of getting this picture!", icon_url=ctx.author.avatar_url)
            embed.set_image(url="https://i.imgur.com/KFOR8YJ.jpeg")
            db.execute("UPDATE luckydogs SET (LuckyDogs, LastUpdated) = (?, ?) WHERE UserID = ?", LuckyDogs[0][0] + 1, datetime.utcnow(), ctx.author.id)
            await ctx.send(embed=embed)

    @command(name="notanimposter", aliases=["nai", "amonguscrew", "crewmate"], brief="Shows a user as not the imposter!")
    @cooldown(1, 4, BucketType.user)
    async def not_an_imposter(self, ctx, *, target: Optional[str]):
        """Among Us Command - Shows a user as `not the imposter`\nI SWEAR I SAW HIM VENT! He wasn't an imposter..."""
        target = target or ctx.author

        # Checks if the target is an "@everyone" or "@here" ping, so Doob doesn't ping the entire server.
        if target == "@everyone" or target == "@here":
            await ctx.send("nope, no ping pong here.")

        else:
            await ctx.send(f". 　　　。　　　　•　 　ﾟ　　。 　　.\n　　　.　　　 　　.　　　　　。　　 。　. 　\n\n.　　 。　　　　　 ඞ 。 . 　　 • 　　　　•\n\n　　ﾟ　　 {target} was not An Impostor.　 。　.\n\n　　'　　　 1 Impostor remain 　 　　。\n\n　　ﾟ　　　.　　　. ,　　　　.　 .")


    @command(name="animposter", aliases=["ai", "amongusimposter", "imposter"], brief="Shows a user as the imposter!")
    @cooldown(1, 4, BucketType.user)
    async def an_imposter(self, ctx, *, target: Optional[str]):
        """Among Us Command - Shows a user as `the imposter`\nI SWEAR I SAW HIM VENT! He was an imposter. I knew it!!!"""
        target = target or ctx.author

        if target == "@everyone" or target == "@here":
            await ctx.send("nope, no ping pong here.")

        else:
            await ctx.send(f". 　　　。　　　　•　 　ﾟ　　。 　　.\n　　　.　　　 　　.　　　　　。　　 。　. 　\n\n.　　 。　　　　　 ඞ 。 . 　　 • 　　　　•\n\n　　ﾟ　　 {target} was An Impostor.　 。　.\n\n　　'　　　 0 Impostors remain 　 　　。\n\n　　ﾟ　　　.　　　. ,　　　　.　 .")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")

def setup(bot):
    bot.add_cog(Fun(bot))
