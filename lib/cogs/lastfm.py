from discord.ext.commands import Cog, command, BucketType, cooldown, group
from discord import Embed, Colour

from ..db import db # pylint: disable=relative-beyond-top-level

from aiohttp import request

from datetime import datetime

from typing import Optional

import os
from dotenv import load_dotenv
load_dotenv()

class LastFM(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def fm_search(self, ctx, username: Optional[str]):
        username = username or db.record("SELECT LastfmUsername FROM exp WHERE UserID = ?", ctx.author.id)[0]
        prefix = db.record("SELECT Prefix from guilds WHERE GuildID = ?", ctx.guild.id)

        if db.record("SELECT LastfmUsername FROM exp WHERE UserID = ?", ctx.author.id)[0] == None:
            await ctx.send(f"Your Last.fm username is set to None\nSet it to your username by doing `{prefix[0]}setlastfm`")
            return

        User_URL = f"https://ws.audioscrobbler.com/2.0/?method=user.getinfo&user={username}&api_key={os.environ.get('lastfmkey')}&format=json"
        top_tracks_url = f"https://ws.audioscrobbler.com/2.0/?method=user.gettoptags&user={username}&api_key={os.environ.get('lastfmkey')}&limit=5&format=json"
        loved_tracks_url = f"https://ws.audioscrobbler.com/2.0/?method=user.getlovedtracks&user={username}&api_key={os.environ.get('lastfmkey')}&format=json"
        
        async with request("GET", User_URL) as response:
            if response.status == 200:
                data = (await response.json())['user']

                embed=Embed(title=f"{data['name']}'s Last.fm profile", description=data['url'],
                            colour=ctx.author.colour)

                ts = int(data['registered']['unixtime'])
                            
                fields = [("Play Count:", f"{data['playcount']}", False),
                        ("Country:", data['country'], False),
                        ("Registered since:", datetime.utcfromtimestamp(ts).strftime('%m-%d-%Y | %H:%M:%S'), False)]

                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                async with request("GET", loved_tracks_url) as loved:
                    loved_data = (await loved.json())['lovedtracks']['@attr']

                    embed.add_field(name="Loved Tracks:", value=loved_data['total'], inline=True)


                async with request("GET", top_tracks_url) as tags:
                    tags_data = (await tags.json())['toptags']
                        
                    tags_list = list()

                    for i in tags_data['tag']:
                        tags_list.append(i['name'])

                    if tags_list:
                        embed.add_field(name="Top Tags:", value=', '.join(tags_list))

                if data['type'] == "subscriber":
                    embed.add_field(name="Last.fm Pro Status", value="Subscribed", inline=False)

                if data['image'][3]['#text'] != "": 
                    embed.set_thumbnail(url=data['image'][3]['#text'])

                await ctx.send(embed=embed)

            else:
                await ctx.send(f"The Last.fm API returned a {response.status} status.")

    @group(name="lastfm", aliases=["fm"], brief="Get your Last.fm information.")
    #@cooldown(1, 5, BucketType.user)
    async def lastfm(self, ctx):
        """Request some information on a specific Last.fm User!\n`Username` = Last.fm Username"""
        if ctx.invoked_subcommand is None:
            await self.fm_search(ctx, username=db.record("SELECT LastfmUsername FROM exp WHERE UserID = ?", ctx.author.id)[0])

    @lastfm.command(name="recent", aliases=['recenttracks', 'recentracks'], brief="Gives you the 5 most recent tracks from a user.")
    async def recent_tracks_command(self, ctx, username: Optional[str]):
        username = username or db.record("SELECT LastfmUsername FROM exp WHERE UserID = ?", ctx.author.id)[0]
        prefix = db.record("SELECT Prefix from guilds WHERE GuildID = ?", ctx.guild.id)

        if db.record("SELECT LastfmUsername FROM exp WHERE UserID = ?", ctx.author.id)[0] == None:
            await ctx.send(f"Your Last.fm username is set to None\nSet it to your username by doing `{prefix[0]}setlastfm`")
            return

        recent_tracks_url = f"https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={username}&api_key={os.environ.get('lastfmkey')}&format=json&limit=5"
    
        async with request("GET", recent_tracks_url) as response:
            data = (await response.json())['recenttracks']

            llist = list()

            for i in data['track']:
                llist.append(f"‣ {i['name']}")

            if llist:
                embed=Embed(title=f"{data['@attr']['user']}'s 5 recent tracks", 
                            description='\n'.join(llist), colour=ctx.author.colour)

                await ctx.send(embed=embed)


            else:
                embed=Embed(title=f"⚠ - No recent tracks found for {data['@attr']['user']}.", colour=ctx.author.colour)

                message = await ctx.send(embed=embed)
            
                await message.add_reaction("⚠️")

    @lastfm.command(name="search", brief="Search a last.fm account.")
    async def search_command(self, ctx, username: Optional[str]):
        username = username or db.record("SELECT LastfmUsername FROM exp WHERE UserID = ?", ctx.author.id)[0]

        await self.fm_search(ctx, username)

    @command(name="setlastfm", aliases=["setfm"], brief="Sets your Last.fm username.")
    @cooldown(1, 5, BucketType.user)
    async def set_overwatch_profile(self, ctx, username: Optional[str]):
        """Sets your Last.fm username for `doob/lastfm`"""

        if username != None:
            embed=Embed(title="Setting Last.fm username:", description=username, colour=ctx.author.colour)

            embed.set_thumbnail(url=ctx.author.avatar_url)

            db.execute("UPDATE exp SET LastfmUsername = ? WHERE UserID = ?", username, ctx.author.id)
            db.commit()

            await ctx.send(embed=embed)

        else:
            username =  db.record("SELECT LastfmUsername FROM exp WHERE UserID = ?", ctx.author.id)
            embed=Embed(title="Your Last.fm username", description=username[0], 
                        colour=ctx.author.colour)

            embed.set_thumbnail(url=ctx.author.avatar_url)

            await ctx.send(embed=embed)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("lastfm")

def setup(bot):
	bot.add_cog(LastFM(bot))