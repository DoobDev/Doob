from discord.ext.commands import Cog, command, BucketType, cooldown, group
from discord import Embed, Colour

from ..db import db  # pylint: disable=relative-beyond-top-level

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
        username = (
            username
            or db.record(
                "SELECT LastfmUsername FROM users WHERE UserID = ?", ctx.author.id
            )[0]
        )
        prefix = db.record("SELECT Prefix from guilds WHERE GuildID = ?", ctx.guild.id)

        if (
            db.record(
                "SELECT LastfmUsername FROM users WHERE UserID = ?", ctx.author.id
            )[0]
            == None
        ):
            await ctx.reply(
                f"Your Last.fm username is set to None\nSet it to your username by doing `{prefix[0]}setlastfm`"
            )
            return

        User_URL = f"https://ws.audioscrobbler.com/2.0/?method=user.getinfo&user={username}&api_key={os.environ.get('lastfmkey')}&format=json"
        top_tracks_url = f"https://ws.audioscrobbler.com/2.0/?method=user.gettoptags&user={username}&api_key={os.environ.get('lastfmkey')}&limit=5&format=json"
        loved_tracks_url = f"https://ws.audioscrobbler.com/2.0/?method=user.getlovedtracks&user={username}&api_key={os.environ.get('lastfmkey')}&format=json"
        recent_tracks_url = f"https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={username}&api_key={os.environ.get('lastfmkey')}&format=json&limit=1"

        async with request("GET", User_URL) as response:
            if response.status == 200:
                data = (await response.json())["user"]

                embed = Embed(
                    title=f"{data['name']}'s Last.fm profile",
                    description=data["url"],
                    colour=ctx.author.colour,
                )

                ts = int(data["registered"]["unixtime"])

                fields = [
                    ("Play Count:", f"{data['playcount']}", True),
                    ("Country:", data["country"], True),
                    (
                        "Registered since:",
                        datetime.utcfromtimestamp(ts).strftime("%m-%d-%Y | %H:%M:%S"),
                        True,
                    ),
                ]

                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                async with request("GET", loved_tracks_url) as loved:
                    loved_data = (await loved.json())["lovedtracks"]["@attr"]

                    embed.add_field(
                        name="Loved Tracks:", value=loved_data["total"], inline=True
                    )

                async with request("GET", top_tracks_url) as tags:
                    tags_data = (await tags.json())["toptags"]

                    tags_list = list()

                    for i in tags_data["tag"]:
                        tags_list.append(i["name"])

                    if tags_list:
                        embed.add_field(name="Top Tags:", value=", ".join(tags_list))

                async with request("GET", recent_tracks_url) as recent:
                    recent_data = (await recent.json())["recenttracks"]

                    embed.add_field(
                        name="Most Recent Track:",
                        value=f"{recent_data['track'][0]['artist']['#text']} - {recent_data['track'][0]['name']}",
                        inline=False,
                    )

                if data["type"] == "subscriber":
                    embed.add_field(
                        name="Last.fm Pro Status", value="Subscribed", inline=False
                    )

                if data["image"][3]["#text"] != "":
                    embed.set_thumbnail(url=data["image"][3]["#text"])

                await ctx.reply(embed=embed)

            else:
                await ctx.reply(f"The Last.fm API returned a {response.status} status.")

    @group(name="lastfm", aliases=["fm"], brief="Get your Last.fm information.")
    # @cooldown(1, 5, BucketType.user)
    async def lastfm(self, ctx):
        """Request some information on a specific Last.fm User!\n`Username` = Last.fm Username"""
        if ctx.invoked_subcommand is None:
            await self.fm_search(
                ctx,
                username=db.record(
                    "SELECT LastfmUsername FROM users WHERE UserID = ?", ctx.author.id
                )[0],
            )

    @lastfm.command(name="--np", aliases=["-np", "np"])
    async def now_playing_command(self, ctx, username: Optional[str]):
        username = (
            username
            or db.record(
                "SELECT LastfmUsername FROM users WHERE UserID = ?", ctx.author.id
            )[0]
        )
        prefix = db.record("SELECT Prefix from guilds WHERE GuildID = ?", ctx.guild.id)

        if (
            db.record(
                "SELECT LastfmUsername FROM users WHERE UserID = ?", ctx.author.id
            )[0]
            == None
        ):
            await ctx.reply(
                f"Your Last.fm username is set to None\nSet it to your username by doing `{prefix[0]}setlastfm`"
            )
            return

        now_playing_url = f"https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={username}&api_key={os.environ.get('lastfmkey')}&format=json&limit=1"

        async with request("GET", now_playing_url) as response:
            data = (await response.json())["recenttracks"]

            llist = list()

            for i in data["track"]:
                llist.append(f"‣ {i['name']} - {i['artist']['#text']}")

            if llist:
                embed = Embed(
                    title=f"{data['@attr']['user']}'s most recent track",
                    description="\n".join(llist),
                    colour=ctx.author.colour,
                )

                await ctx.reply(embed=embed)

            else:
                embed = Embed(
                    title=f"⚠ - No recent tracks found for {data['@attr']['user']}.",
                    colour=ctx.author.colour,
                )

                message = await ctx.reply(embed=embed)

                await message.add_reaction("⚠️")

    @lastfm.command(
        name="recent",
        aliases=["recenttracks", "recentracks"],
        brief="Gives you the 5 most recent tracks from a user.",
    )
    async def recent_tracks_command(self, ctx, username: Optional[str]):
        username = (
            username
            or db.record(
                "SELECT LastfmUsername FROM users WHERE UserID = ?", ctx.author.id
            )[0]
        )
        prefix = db.record("SELECT Prefix from guilds WHERE GuildID = ?", ctx.guild.id)

        if (
            db.record(
                "SELECT LastfmUsername FROM users WHERE UserID = ?", ctx.author.id
            )[0]
            == None
        ):
            await ctx.reply(
                f"Your Last.fm username is set to None\nSet it to your username by doing `{prefix[0]}setlastfm`"
            )
            return

        recent_tracks_url = f"https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={username}&api_key={os.environ.get('lastfmkey')}&format=json&limit=5"

        async with request("GET", recent_tracks_url) as response:
            data = (await response.json())["recenttracks"]

            llist = list()

            for i in data["track"]:
                llist.append(f"‣ {i['name']} - {i['artist']['#text']}")

            if llist:
                embed = Embed(
                    title=f"{data['@attr']['user']}'s 5 recent tracks",
                    description="\n".join(llist),
                    colour=ctx.author.colour,
                )

                await ctx.reply(embed=embed)

            else:
                embed = Embed(
                    title=f"⚠ - No recent tracks found for {data['@attr']['user']}.",
                    colour=ctx.author.colour,
                )

                message = await ctx.reply(embed=embed)

                await message.add_reaction("⚠️")

    @lastfm.group(name="top")
    async def top_group(self, ctx):
        subcommand = ctx.invoked_subcommand
        if (
            subcommand != self.top_albums_command
            and subcommand != self.top_tracks_command
            and subcommand != self.top_artist_command
        ):
            prefix = db.record(
                "SELECT Prefix from guilds WHERE GuildID = ?", ctx.guild.id
            )
            await ctx.reply(
                f"Try these commands instead.\n`{prefix[0]}fm top albums`\n`{prefix[0]}fm top tracks`\n`{prefix[0]}fm top artists`"
            )

    @top_group.command(name="albums")
    async def top_albums_command(self, ctx, username: Optional[str]):
        username = (
            username
            or db.record(
                "SELECT LastfmUsername FROM users WHERE UserID = ?", ctx.author.id
            )[0]
        )

        top_albums_url = f"https://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user={username}&api_key={os.environ.get('lastfmkey')}&format=json&limit=10"
        User_URL = f"https://ws.audioscrobbler.com/2.0/?method=user.getinfo&user={username}&api_key={os.environ.get('lastfmkey')}&format=json"

        async with request("GET", top_albums_url) as response:
            data = (await response.json())["topalbums"]

            llist = list()

            for i in data["album"]:
                llist.append(
                    f"‣ #{i['@attr']['rank']} - {i['artist']['name']} - {i['name']} ({i['playcount']} plays)"
                )

            if llist:
                embed = Embed(
                    title=f"{data['@attr']['user']}'s 10 top albums",
                    description="\n".join(llist),
                    colour=ctx.author.colour,
                )

                embed.set_thumbnail(url=data["album"][0]["image"][3]["#text"])

                async with request("GET", User_URL) as icon:
                    icon_url = (await icon.json())["user"]

                    if icon_url["image"][3]["#text"] != "":
                        embed.set_footer(
                            text=f"last.fm/users/{data['@attr']['user']}",
                            icon_url=icon_url["image"][3]["#text"],
                        )

                await ctx.reply(embed=embed)

            else:
                embed = Embed(
                    title=f"⚠ - No top albums found for {data['@attr']['user']}.",
                    colour=ctx.author.colour,
                )

                message = await ctx.reply(embed=embed)

                await message.add_reaction("⚠️")

    @top_group.command(name="tracks")
    async def top_tracks_command(self, ctx, username: Optional[str]):
        username = (
            username
            or db.record(
                "SELECT LastfmUsername FROM users WHERE UserID = ?", ctx.author.id
            )[0]
        )

        top_tracks_url = f"https://ws.audioscrobbler.com/2.0/?method=user.gettoptracks&user={username}&api_key={os.environ.get('lastfmkey')}&format=json&limit=10"
        User_URL = f"https://ws.audioscrobbler.com/2.0/?method=user.getinfo&user={username}&api_key={os.environ.get('lastfmkey')}&format=json"

        async with request("GET", top_tracks_url) as response:
            data = (await response.json())["toptracks"]

            llist = list()

            for i in data["track"]:
                llist.append(
                    f"‣ #{i['@attr']['rank']} - {i['artist']['name']} - {i['name']} ({i['playcount']} plays)"
                )

            if llist:
                embed = Embed(
                    title=f"{data['@attr']['user']}'s 10 top tracks",
                    description="\n".join(llist),
                    colour=ctx.author.colour,
                )

                embed.set_thumbnail(url=data["track"][0]["image"][3]["#text"])

                async with request("GET", User_URL) as icon:
                    icon_url = (await icon.json())["user"]

                    if icon_url["image"][3]["#text"] != "":
                        embed.set_footer(
                            text=f"last.fm/users/{data['@attr']['user']}",
                            icon_url=icon_url["image"][3]["#text"],
                        )

                await ctx.reply(embed=embed)

            else:
                embed = Embed(
                    title=f"⚠ - No top tracks found for {data['@attr']['user']}.",
                    colour=ctx.author.colour,
                )

                message = await ctx.reply(embed=embed)

                await message.add_reaction("⚠️")

    @top_group.command(name="artists", aliases=["artist"])
    async def top_artist_command(self, ctx, username: Optional[str]):
        username = (
            username
            or db.record(
                "SELECT LastfmUsername FROM users WHERE UserID = ?", ctx.author.id
            )[0]
        )

        top_artists_url = f"https://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user={username}&api_key={os.environ.get('lastfmkey')}&format=json&limit=10"
        User_URL = f"https://ws.audioscrobbler.com/2.0/?method=user.getinfo&user={username}&api_key={os.environ.get('lastfmkey')}&format=json"

        async with request("GET", top_artists_url) as response:
            data = (await response.json())["topartists"]

            llist = list()

            for i in data["artist"]:
                llist.append(
                    f"‣ #{i['@attr']['rank']} - {i['name']} - ({i['playcount']} plays)"
                )

            if llist:
                embed = Embed(
                    title=f"{data['@attr']['user']}'s 10 top artists",
                    description="\n".join(llist),
                    colour=ctx.author.colour,
                )

                embed.set_thumbnail(url=data["artist"][0]["image"][3]["#text"])

                async with request("GET", User_URL) as icon:
                    icon_url = (await icon.json())["user"]

                    if icon_url["image"][3]["#text"] != "":
                        embed.set_footer(
                            text=f"last.fm/users/{data['@attr']['user']}",
                            icon_url=icon_url["image"][3]["#text"],
                        )

                await ctx.reply(embed=embed)

            else:
                embed = Embed(
                    title=f"⚠ - No top artists found for {data['@attr']['user']}.",
                    colour=ctx.author.colour,
                )

                message = await ctx.reply(embed=embed)

                await message.add_reaction("⚠️")

    @lastfm.command(name="search", brief="Search a last.fm account.")
    async def search_command(self, ctx, username: Optional[str]):
        username = (
            username
            or db.record(
                "SELECT LastfmUsername FROM users WHERE UserID = ?", ctx.author.id
            )[0]
        )

        await self.fm_search(ctx, username)

    @lastfm.group(name="artist")
    async def artist_group(self, ctx):
        subcommand = ctx.invoked_subcommand
        if (
            subcommand != self.artist_charts_command
            and subcommand != self.artist_search_command
        ):
            prefix = db.record(
                "SELECT Prefix from guilds WHERE GuildID = ?", ctx.guild.id
            )
            await ctx.reply(
                f"Try these commands instead.\n`{prefix[0]}fm artist charts`\n`{prefix[0]}fm artist search"
            )

    @artist_group.command(name="charts")
    async def artist_charts_command(self, ctx):
        charts_url = f"https://ws.audioscrobbler.com/2.0/?method=chart.gettopartists&api_key={os.environ.get('lastfmkey')}&format=json&limit=10"

        async with request("GET", charts_url) as response:
            data = (await response.json())["artists"]

            llist = list()

            for i in data["artist"]:
                llist.append(f"‣ {i['name']}")

            if llist:
                embed = Embed(
                    title="Top 10 artists on Last.fm",
                    description="\n".join(llist),
                    colour=ctx.author.colour,
                )

                await ctx.reply(embed=embed)

    @artist_group.command(name="search")
    async def artist_search_command(self, ctx, *, artist: str):
        info_url = f"https://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={artist}&api_key={os.environ.get('lastfmkey')}&format=json"
        toptracks = f"https://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist={artist}&api_key={os.environ.get('lastfmkey')}&format=json&limit=5"
        topalbums = f"https://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&artist={artist}&api_key={os.environ.get('lastfmkey')}&format=json&limit=5"
        # spotify_search = f"https://api.spotify.com/v1/search&type=artist&q={artist}&limit=1"

        async with request("GET", info_url) as response:
            if response.status == 200:
                data = (await response.json())["artist"]

                embed = Embed(
                    title=f"{data['name']} info on Last.fm",
                    description=data["url"],
                    colour=ctx.author.colour,
                )

                fields = [
                    ("Listeners:", data["stats"]["listeners"], True),
                    ("Play Count:", data["stats"]["playcount"], True),
                    ("Wiki:", data["bio"]["links"]["link"]["href"], False),
                ]

                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                similar = list()

                for i in data["similar"]["artist"]:
                    similar.append(i["name"])

                if similar:
                    embed.add_field(name="Similar Artists:", value=", ".join(similar))

                async with request("GET", toptracks) as response:
                    if response.status == 200:
                        toptracks = (await response.json())["toptracks"]

                        tracks = list()

                        for i in toptracks["track"]:
                            tracks.append(
                                f"‣ #{i['@attr']['rank']} {i['name']}: Play Count ‣ {i['playcount']}"
                            )

                        if tracks:
                            embed.add_field(
                                name="Top Tracks:",
                                value="\n".join(tracks),
                                inline=False,
                            )

                async with request("GET", topalbums) as response:
                    if response.status == 200:
                        topalbums = (await response.json())["topalbums"]

                        albums = list()

                        for i in topalbums["album"]:
                            albums.append(
                                f"‣ {i['name']}: Play Count ‣ {i['playcount']}"
                            )

                        if albums:
                            embed.add_field(
                                name="Top Albums:",
                                value="\n".join(albums),
                                inline=False,
                            )

                    # async with request("GET", spotify_search, headers={"Authorization Bearer:": os.environ.get('spotify_id'), 'Content_Type': 'application/json'}) as response:
                    #     if response.status == 200:
                    #         data = (await response.json(content_type=None))['artists']['items'][0]

                    #         embed.set_thumbnail(url=data['images'][0]['url'])

                    # else:
                    #     await ctx.reply(f"spotify sucks {response.status} error")

                await ctx.reply(embed=embed)

    @command(name="setlastfm", aliases=["setfm"], brief="Sets your Last.fm username.")
    @cooldown(1, 5, BucketType.user)
    async def set_lastfm_username(self, ctx, username: Optional[str]):
        """Sets your Last.fm username for `d!lastfm`"""

        if username != None:
            embed = Embed(
                title="Setting Last.fm username:",
                description=username,
                colour=ctx.author.colour,
            )

            embed.set_thumbnail(url=ctx.author.avatar_url)

            db.execute(
                "UPDATE users SET LastfmUsername = ? WHERE UserID = ?",
                username,
                ctx.author.id,
            )
            db.commit()

            await ctx.reply(embed=embed)

        else:
            username = db.record(
                "SELECT LastfmUsername FROM users WHERE UserID = ?", ctx.author.id
            )
            embed = Embed(
                title="Your Last.fm username",
                description=username[0],
                colour=ctx.author.colour,
            )

            embed.set_thumbnail(url=ctx.author.avatar_url)

            await ctx.reply(embed=embed)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("lastfm")


def setup(bot):
    bot.add_cog(LastFM(bot))
