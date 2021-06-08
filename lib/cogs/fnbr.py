import datetime
from discord.ext.commands import Cog, command, cooldown, BucketType

from discord import Embed

from ..db import db  # pylint: disable=relative-beyond-top-level
from aiohttp import request

import json

with open("config.json") as config_file:
    config = json.load(config_file)

import os
from dotenv import load_dotenv

load_dotenv()


class Fnbr(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fnbr")

    @command(name="fortniteskin", aliases=["skinsearch", "skin"])
    @cooldown(1, 5, BucketType.user)
    async def fort_skin_search(self, ctx, *, skin: str):
        """Search a Fortnite skin using fnbr.co"""
        # common, uncommon, rare, epic, legendary, shadow, icon series
        URL = f"https://fnbr.co/api/images?search={skin}"

        async with request(
            "GET",
            URL,
            headers={
                "x-api-key": os.environ.get("fnbr_key"),
                "Content-Type": "application/json",
            },
        ) as response:
            if response.status == 200:
                data1 = (await response.json())["data"]
                data2 = (await response.json())["data"][0]

                if data2["rarity"] == "common":
                    color = 0xB3B3B3

                elif data2["rarity"] == "uncommon":
                    color = 0x7EE700

                elif data2["rarity"] == "rare":
                    color = 0x00EEFC

                elif data2["rarity"] == "epic":
                    color = 0xDB33FF

                elif data2["rarity"] == "legendary":
                    color = 0xFBA14C

                elif data2["rarity"] == "shadow":
                    color = 0xEB37A7

                elif data2["rarity"] == "icon_series":
                    color = 0x6DDAEB

                else:
                    color = ctx.author.color

                embed = Embed(
                    title=data1[0]["name"],
                    description="<:icon_vbucks:851675167993102356> Price: "
                    + data2["price"]
                    + "\nType: "
                    + data2["readableType"]
                    + "\nRarity: "
                    + data2["rarity"].capitalize(),
                    colour=color,
                )

                embed.set_image(url=data2["images"]["featured"])
                embed.set_thumbnail(url=data2["images"]["icon"])

                embed.set_author(
                    name="Provided by fnbr.co!",
                    icon_url="https://image.fnbr.co/logo/logo_75x.png",
                    url="https://fnbr.co",
                )

                embed.set_footer(
                    text="use code 'matt'! #EpicPartner", icon_url=ctx.author.avatar_url
                )

                await ctx.send(embed=embed)
            else:
                await ctx.send(f"The fnbr.co API sent a {response.status} status :/")

    @command(
        name="fortniteshop",
        aliases=["fnshop", "shop"],
        brief="Shows the current Fortnite Shop.",
    )
    async def fortnite_shop_command(self, ctx):
        """Shows the current Fortnite Item Shop courtacy of https://fnbr.co\nuse code `matt` in the fortnite item shop :O #ad"""

        URL = "https://fnbr.co/api/shop"

        async with request(
            "GET",
            URL,
            headers={
                "x-api-key": os.environ.get("fnbr_key"),
                "Content-Type": "application/json",
            },
        ) as response:
            if response.status == 200:
                data = (await response.json())["data"]
    
                embed = Embed(
                    title="The Current Fortnite Item Shop",
                    colour=ctx.author.color,
                )

                for item in data["featured"]:
                    embed.add_field(name=item["name"], value="Price: " + item["price"] + "\nType: " + item["readableType"] + "\nRarity: " + item["rarity"].capitalize())

                await ctx.send(embed=embed)

            else:
                await ctx.send(f"The fnbr.co API sent a {response.status} status :/")


def setup(bot):
    bot.add_cog(Fnbr(bot))
