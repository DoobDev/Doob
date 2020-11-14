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
        await ctx.send(f"{choice(('Hello', 'Hi', 'Hey'))} {ctx.author.mention}!")

    @command(name="dice", aliases=["roll", "rolldice"], brief="Roll some dice!")
    @cooldown(1, 10, BucketType.user)
    async def roll_dice(self, ctx, die_string: str):
        """Role some dice, (number)d(number) syntax."""
        dice, value = (int(term) for term in die_string.split("d"))

        if dice <= 40:
            rolls = [randint(1, value) for i in range(dice)]

            await ctx.send(" + ".join([str(r) for r in  rolls]) + f" = {sum(rolls)}")
        else:
            await ctx.send("Please roll a lower number of dice.", delete_after=10)

    @command(name="echo", aliases=["say"], brief="Make Doob say something!")
    @cooldown(1, 10, BucketType.user)
    async def echo_message(self, ctx, *, message):
        """Make Doob say a message! | `Patreon Only`"""
        homeGuild = self.bot.get_guild(702352937980133386)
        patreonRole = get(homeGuild.roles, id=757041749716893739)  # Patreon role ID.

        member = []

        for pledger in homeGuild.members:
            if pledger == ctx.author:
                member = pledger

        if ctx.author in homeGuild.members:
            if patreonRole in member.roles:
                    await ctx.send(message)
                    print(f"{ctx.author.name} used the Echo command and said {message}")

            else:
                await ctx.send("You are not a Patron to Doob, subscribe to any of the tiers at <https://patreon.com/doobdev> to gain access to this command.")

        else:
            await ctx.send("You are not a Patron to Doob, subscribe to any of the tiers at <https://patreon.com/doobdev> to gain access to this command.")

    @command(name="fact", aliases=["dogfact", "facts"], brief="Learn a random fact about dogs!")
    @cooldown(3, 10, BucketType.user)
    async def dog_fact(self, ctx):
        """Get a wacky dog fact"""
        URL = "https://some-random-api.ml/facts/dog"

        async with request("GET", URL, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                embed = Embed(title="Dog Fact!", description=data["fact"], colour=ctx.author.colour)
                embed.set_footer(text=f"{ctx.author} requested this fact!", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"Dog fact API sent a {response.status} status.")

    @command(name="luckydog", aliases=["ldog"], brief="Get an instant Lucky Dog!")
    @cooldown(2, 5, BucketType.user)
    async def lucky_dog_image(self, ctx, *, dog: Optional[str]):
        """Shows the lucky dogs possible!\nIsn't eligable for the Nitro Giveaways\n`Patreon` permission required"""
        homeGuild = self.bot.get_guild(702352937980133386)
        patreonRole = get(homeGuild.roles, id=757041749716893739)

        member = []

        for pledger in homeGuild.members:
            if pledger == ctx.author:
                member = pledger

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
            
            else:
                await ctx.send("This is a Patreon (<https://patreon.com/doobdev>) only command.")
        
        else:
            await ctx.send("This is a Patreon (<https://patreon.com/doobdev>) only command.")

    @command(name="luckydogs", aliases=["dogscaught", "ldc", "ld", "checkdogs", "lds"], brief="Check how many Lucky Dogs you have gotten!")
    @cooldown(2, 5, BucketType.user)
    async def check_lucky_dogs(self, ctx, *, target: Optional[Member]):
        """Check how many Lucky dogs you have gotten in the last month!"""
        target = target or ctx.author

        LuckyDogs = db.records("SELECT LuckyDogs FROM luckydogs WHERE UserID = ?", target.id)

        embed = Embed(title=f"{target.name} has gotten:", description=f"{str(LuckyDogs[0][0])} Lucky Dog(s) this month.", colour=target.colour)
        embed.set_footer(text=f"{ctx.author.name} requested this. | Doob", icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=target.avatar_url)
        await ctx.send(embed=embed)

    @command(name="dog", aliases=["dogimage"], brief="See a random picture of a dog!")
    @cooldown(2, 5, BucketType.user)
    async def dog_image(self, ctx):
        """So this is what you came for...\nGives you a random picture of a dog!"""
        LuckyDogs = db.records("SELECT LuckyDogs FROM luckydogs WHERE UserID = ?", ctx.author.id)

        homeGuild = self.bot.get_guild(702352937980133386)
        patreonRole = get(homeGuild.roles, id=757041749716893739)
        
        member = []
                       
        URL = "https://dog.ceo/api/breeds/image/random"

        for pledger in homeGuild.members:
            if pledger == ctx.author:
                member = pledger


        if ctx.author in homeGuild.members:
            if patreonRole in member.roles:
                random = randint(1,53)

                if random != 50 and random != 51 and random != 52 and random != 53:
                    async with request("GET", URL, headers={}) as response:
                        if response.status == 200:
                            data = await response.json()
                            embed = Embed(title="Dog Picture!", colour=ctx.author.colour)
                            #embed.set_footer(text=f"DEBUG: L_DOG: {random}")
                            embed.set_image(url=data["message"])
                            await ctx.send(embed=embed)
                
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
                await self.lucky_dogs(ctx)
                
            
        else:
            await self.lucky_dogs(ctx)

    async def lucky_dogs(self, ctx):
        random = randint(1,503)
        patreon_ad = randint(1, 4)

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
