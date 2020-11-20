from discord.ext.commands import Cog, command, BucketType, cooldown
from discord import Embed, Colour, Member

from ..db import db # pylint: disable=relative-beyond-top-level

from aiohttp import request

from datetime import datetime

import json

from typing import Optional

import os
from dotenv import load_dotenv
load_dotenv()

class Bio(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="bio", aliases=["dbio", "discordbio"], brief="Get Twitch stream information.")
    @cooldown(1, 5, BucketType.user)
    async def discord_bio_command(self, ctx, *, target: Optional[Member]):
        """Lookup your Discord.bio profile information here.""" 

        target = target or ctx.author

        User_URL = f"https://api.discord.bio/user/details/{target.id}"
        async with request("GET", User_URL) as response:
            if response.status == 200:
                data = (await response.json())['payload']['user']

                title = f"{target.display_name}'s discord.bio profile"
                desc = f"https://dsc.bio/{data['details']['slug']}"

                if data['details']['premium'] == True:
                    title = f"{target.display_name}'s discord.bio profile 💎"
                    desc = f"💎 https://dsc.bio/{data['details']['slug']} 💎"

                embed=Embed(title=title, description=desc,
                colour=target.colour, timestamp=datetime.utcnow())

                fields = [("Bio", data['details']['description'], False),
                          ("Location", data['details']['location'], True),
                          ("Likes", f"💙 {data['details']['likes']}", True),
                          ("Verified Status", data['details']['verified'], True),
                          ("Premium Status", data['details']['premium'], True),
                          ("Occupation", data['details']['occupation'], True),
                          ("Birthday", data['details']['birthday'], True),
                          ("Email", f"||{data['details']['email']}||", False)]

                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                embed.set_thumbnail(url=target.avatar_url)
                
                if data['details']['banner'] != None:
                    embed.set_image(url=data['details']['banner'])

                await ctx.send(embed=embed)

            else:
                await ctx.send(f"Discord.bio API returned a {response.status} status.")

    @Cog.listener() 
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("bio")

def setup(bot):
	bot.add_cog(Bio(bot))