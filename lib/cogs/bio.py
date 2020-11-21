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

        # Target = the target the user specified, if there is nobody they specified, it defaults back to the author.
        target = target or ctx.author

        # Discord.bio's API URL
        User_URL = f"https://api.discord.bio/user/details/{target.id}"
        
        async with request("GET", User_URL) as response:
            if response.status == 200: # This is to make sure the API is working.
                data = (await response.json())['payload']['user'] # This gets the user's information from the .json file the API gives you.

                title = f"{target.display_name}'s discord.bio profile" # Sets the title for the embed
                desc = f"https://dsc.bio/{data['details']['slug']}" # Sets the description for the embed

                if data['details']['premium'] == True: # If they are a premium subscriber to Discord.bio
                    title = f"{target.display_name}'s discord.bio profile 💎" # Give them this title/description
                    desc = f"💎 https://dsc.bio/{data['details']['slug']} 💎"

                embed=Embed(title=title, description=desc,
                colour=target.colour, timestamp=datetime.utcnow()) # Embed setup.

                # This is where all the data comes in, pretty self explainitory if you look through the .json file
                # given to you by the API.

                fields = [("Bio", data['details']['description'], False),
                          ("Location", data['details']['location'], True),
                          ("Likes", f"💙 {data['details']['likes']}", True),
                          ("Verified Status", data['details']['verified'], True),
                          ("Premium Status", data['details']['premium'], True),
                          ("Occupation", data['details']['occupation'], True),
                          ("Birthday", data['details']['birthday'], True),
                          ("Email", f"||{data['details']['email']}||", False)]

                # Adds all the items from the `fields` variable into the embed. 
                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                # Sets the embed thumbnail to the target's avatar on Discord
                embed.set_thumbnail(url=target.avatar_url)
                
                # If they have a banner on Discord.bio, show it as the "image" in the embed.
                if data['details']['banner'] != None:
                    embed.set_image(url=data['details']['banner'])

                await ctx.send(embed=embed)

            else: # If the API status is something other then a 200, it sends you a message telling you which status it sent
                await ctx.send(f"Discord.bio API returned a {response.status} status.")

    @Cog.listener() 
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("bio")

def setup(bot):
	bot.add_cog(Bio(bot))