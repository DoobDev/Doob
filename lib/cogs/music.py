"""
DONT MOVE IF YOU HAVE SET UP DOOB MUSIC
"""
import asyncio
import typing
import re
import random
from enum import Enum

import aiohttp
import discord
import wavelink
from discord.ext import commands

from datetime import datetime

URL_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
LYRICS_URL = "https://some-random-api.ml/lyrics?title="
HZ_BANDS = (20, 40, 63, 100, 150, 250, 400, 450, 630, 1000, 1600, 2500, 4000, 10000, 16000)
OPTIONS = {
    "1️⃣": 0,
    "2⃣": 1,
    "3⃣": 2,
    "4⃣": 3,
    "5⃣": 4,
}


class AlreadyConnected(commands.CommandError):
    pass


class NoVoiceChannel(commands.CommandError):
    pass


class QueueIsEmpty(commands.CommandError):
    pass


class NoTracksFound(commands.CommandError):
    pass


class PlayerPaused(commands.CommandError):
    pass


class PlayerPlaying(commands.CommandError):
    pass


class NoMoreTracks(commands.CommandError):
    pass


class NoPreviousTrack(commands.CommandError):
    pass


class InvalidRepeatMode(commands.CommandError):
    pass

class volumeTooLow(commands.CommandError):
    pass

class volumeTooHigh(commands.CommandError):
    pass

class MaxVolume(commands.CommandError):
    pass

class MinVolume(commands.CommandError):
    pass

class NoLyricsFound(commands.CommandError):
    pass



class RepeatMode(Enum):
    NONE = 0
    ONE = 1
    ALL = 2


class Queue:
    def __init__(self):
        self._queue = []
        self.position = 0
        self.repeat_mode = RepeatMode.NONE

    @property
    def is_empty(self):
        return not self._queue

    @property
    def first_track(self):
        if not self._queue:
            raise QueueIsEmpty

        return self._queue[0]

    @property
    def current_track(self):
        if not self._queue:
            raise QueueIsEmpty

        return self._queue[self.position]

    @property
    def upcoming(self):
        if not self._queue:
            raise QueueIsEmpty

        return self._queue[self.position + 1 :]

    @property
    def history(self):
        if not self._queue:
            raise QueueIsEmpty

        return self._queue[: self.position]

    @property
    def length(self):
        return len(self._queue)

    def add(self, *args):
        self._queue.extend(args)

    def get_next_track(self):
        if not self._queue:
            raise QueueIsEmpty

        self.position += 1

        if self.position < 0:
            return None

        elif self.position > len(self._queue) - 1:
            if self.repeat_mode == RepeatMode.ALL:
                self.position = 0
            else:
                return None

        return self._queue[self.position]

    def shuffle(self):
        if not self._queue:
            raise QueueIsEmpty

        upcoming = self.upcoming
        random.shuffle(upcoming)

        self._queue = self._queue[: self.position + 1]
        self._queue.extend(upcoming)

    def set_repeat_mode(self, mode):
        if mode == "none":
            self.repeat_mode = RepeatMode.NONE
        elif mode == "1":
            self.repeat_mode = RepeatMode.ONE
        elif mode == "all":
            self.repeat_mode = RepeatMode.ALL

    def empty(self):
        self._queue.clear()


class Player(wavelink.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = Queue()

    async def connect(self, ctx, channel=None):
        if self.is_connected:
            raise AlreadyConnected

        if (channel := getattr(ctx.author.voice, "channel", channel)) is None:
            raise NoVoiceChannel

        await super().connect(channel.id)

        return channel

    async def teardown(self):
        try:
            await self.destroy()

        except KeyError:
            pass

    async def add_tracks(self, ctx, tracks):
        if not tracks:
            raise NoTracksFound

        if isinstance(tracks, wavelink.TrackPlaylist):
            self.queue.add(*tracks.tracks)

        elif len(tracks) == 1:
            self.queue.add(tracks[0])
            await ctx.send(f"Track ({tracks[0].title}) added.")

        else:
            if (track := await self.choose_track(ctx, tracks)) is not None:
                self.queue.add(track)

                await ctx.send(f"Track ({track.title}) added.")

        if not self.is_playing:
            await self.start_playback()

    async def choose_track(self, ctx, tracks):
        def _check(r, u):
            return (
                r.emoji in OPTIONS.keys() and u == ctx.author and r.message.id == msg.id
            )

        embed = discord.Embed(
            title="Choose a song",
            description=(
                "\n".join(
                    f"**{i+1}.** {t.title} ({t.length//60000}:{str(t.length%60).zfill(2)})"
                    for i, t in enumerate(tracks[:5])
                )
            ),
            colour=ctx.author.colour,
            timestamp=datetime.utcnow(),
        )

        embed.set_author(name="Search Results")
        embed.set_footer(
            text=f"Searched by {ctx.author.display_name}",
            icon_url=ctx.author.avatar_url,
        )

        msg = await ctx.send(embed=embed)
        for emoji in list(OPTIONS.keys())[: min(len(tracks), len(OPTIONS))]:
            await msg.add_reaction(emoji)

        try:
            reaction, _ = await self.bot.wait_for(
                "reaction_add", timeout=60.0, check=_check
            )

        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.message.delete()

        else:
            await msg.delete()
            return tracks[OPTIONS[reaction.emoji]]

    async def start_playback(self):
        await self.play(self.queue.first_track)

    async def advance(self):
        try:
            if (track := self.queue.get_next_track()) is not None:
                await self.play(track)

        except QueueIsEmpty:
            pass

    async def repeat_track(self):
        await self.play(self.queue.current_track)


class Music(commands.Cog, wavelink.WavelinkMixin):
    def __init__(self, bot):
        self.wavelink = wavelink.Client(bot=bot)
        self.bot = bot
        self.bot.loop.create_task(self.start_nodes())

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if (
            not member.bot
            and after.channel is None
            and not [m for m in before.channel.members if not m.bot]
        ):
            await self.get_player(member.guild).teardown()

    @wavelink.WavelinkMixin.listener()
    async def on_node_ready(self, node):
        print(f"Wavelink node {node.identifier} ready.")

    @wavelink.WavelinkMixin.listener("on_track_stuck")
    @wavelink.WavelinkMixin.listener("on_track_end")
    @wavelink.WavelinkMixin.listener("on_track_exception")
    async def on_player_stop(self, node, payload):
        if payload.player.queue.repeat_mode == RepeatMode.ONE:
            await payload.player.repeat_track()

        else:
            await payload.player.advance()

    async def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.DMChannel):
            await ctx.send("Music commands can't be used in DMs.")
            return False

        return True

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        nodes = {
            "MAIN": {
                "host": "127.0.0.1",
                "port": 2335,
                "rest_uri": "http://127.0.0.1:2335",
                "password": "youshallnotpass",
                "identifier": "MAIN",
                "region": "us_central",
            }
        }

        for node in nodes.values():
            await self.wavelink.initiate_node(**node)

    def get_player(self, obj):
        if isinstance(obj, commands.Context):
            return self.wavelink.get_player(obj.guild.id, cls=Player, context=obj)

        elif isinstance(obj, discord.Guild):
            return self.wavelink.get_player(obj.id, cls=Player)

    @commands.command(
        name="connect", aliases=["join"], brief="Connect Doob to a Voice Channel"
    )
    async def connect_command(
        self, ctx, *, channel: typing.Optional[discord.VoiceChannel]
    ):
        """Connect Doob to a Voice Channel to be able to listen to music!"""
        player = self.get_player(ctx)
        channel = await player.connect(ctx, channel)
        await ctx.send(f"Connected to {channel.name}!")

    @connect_command.error
    async def connect_command_error(self, ctx, exc):
        if isinstance(exc, AlreadyConnected):
            await ctx.send("Already connected to a voice channel.")
        elif isinstance(exc, NoVoiceChannel):
            await ctx.send("No voice channel could be found.")

    @commands.command(
        name="disconnect", aliases=["leave"], brief="Make Doob leave a voice channel."
    )
    async def disconnect_command(self, ctx):
        """Disonnect Doob from a voice channel."""
        player = self.get_player(ctx)
        await player.teardown()
        await ctx.send("Disconnected")

    @commands.command(name="play", brief="Plays a song.")
    async def play_command(self, ctx, *, query: typing.Optional[str]):
        """Lets you be able to search a song, or put in a YouTube link so you can listen to music.\nIf Doob isn't already in  the voice channel, it will connect.\nIf Doob is already connected, it will queue up the song you requested."""
        player = self.get_player(ctx)

        if not player.is_connected:
            await player.connect(ctx)

        if query is None:
            if not player.is_paused:
                raise PlayerPlaying

            if player.queue.is_empty:
                raise QueueIsEmpty

            await player.set_pause(False)
            await ctx.send("Music resumed. ▶")

        else:
            query = query.strip("<>")
            if not re.match(URL_REGEX, query):
                query = f"ytsearch:{query}"

            await player.add_tracks(ctx, await self.wavelink.get_tracks(query))

    @play_command.error
    async def play_command_error(self, ctx, exc):
        if isinstance(exc, PlayerPlaying):
            await ctx.send("Music is already playing.")

        if isinstance(exc, QueueIsEmpty):
            await ctx.send("The queue is empty.")

    @commands.command(name="resume", brief="Resumes a song from being paused.")
    async def resume_command(self, ctx):
        """After pausing a song, you can resume it with this command."""
        player = self.get_player(ctx)

        if not player.is_paused:
            raise PlayerPlaying

        if player.queue.is_empty:
            raise QueueIsEmpty

        await player.set_pause(False)
        await ctx.send("Music resumed. ▶")

    @commands.command(name="pause", brief="Pauses a song while it is playing.")
    async def pause_command(self, ctx):
        player = self.get_player(ctx)

        if player.is_paused:
            raise PlayerPaused

        await player.set_pause(True)

        await ctx.send("Music paused. ⏸")

    @pause_command.error
    async def pause_command_error(self, ctx, exc):
        if isinstance(exc, PlayerPaused):
            await ctx.send("Music is already paused. ⏸")

    @commands.command(name="stop", brief="Stops the music, and clears the queue.")
    async def stop_command(self, ctx):
        """Stops the music and clears the queue, Doob also leaves the Voice Channel."""
        player = self.get_player(ctx)

        player.queue.empty()

        await player.stop()
        await ctx.send("Music stopped, queue cleared. ⏹")

    @commands.command(name="next", aliases=["skip"], brief="Skips the current song.")
    async def next_command(self, ctx):
        """Skips the current song and goes to the next song in the queue if there is one."""
        player = self.get_player(ctx)

        if not player.queue.upcoming:
            raise NoMoreTracks

        await player.stop()
        await ctx.send("Skipping track. ▶")

    @next_command.error
    async def next_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("Queue is empty, can't skip track.")

        if isinstance(exc, NoMoreTracks):
            await ctx.send("No more tracks in the queue, can't skip track.")

    @commands.command(name="previous", brief="Goes to the previous track in the queue.")
    async def previous_command(self, ctx):
        """Plays the previous track in the queue."""
        player = self.get_player(ctx)

        if not player.queue.history:
            raise NoPreviousTrack

        player.queue.position -= 2
        await player.stop()
        await ctx.send("Previous track is now playing. ◀")

    @previous_command.error
    async def previous_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("Queue is empty, can't go to the previous track.")

        if isinstance(exc, NoPreviousTrack):
            await ctx.send(
                "No previous track in the queue, can't go to the previous track."
            )

    @commands.command(name="shuffle", brief="Shuffles the queue.")
    async def shuffle_queue_command(self, ctx):
        """Shuffles the upcoming queue, doesn't stop the current song."""
        player = self.get_player(ctx)

        player.queue.shuffle()

        await ctx.send("Queue shuffled. 🔀")

    @shuffle_queue_command.error
    async def shuffle_queue_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("The queue is empty, can't shuffle it.")

    @commands.command(name="repeat", aliases=["loop"], brief="Lets you repeat.")
    async def repeat_command(self, ctx, mode: str):
        """Lets you repeat.\n`none` = Stops repeating\n`1` = repeats the current song\n`all` = repeats the queue."""
        if mode not in ("none", "1", "all"):
            raise InvalidRepeatMode

        player = self.get_player(ctx)
        player.queue.set_repeat_mode(mode)
        await ctx.send(f"The repeat mode has been set to {mode}.")

    @commands.command(name="queue", brief="Shows the queue.")
    async def queue_command(self, ctx, show: typing.Optional[int] = 10):
        """Shows the queue for the current server."""
        player = self.get_player(ctx)

        if player.queue.is_empty:
            raise QueueIsEmpty

        embed = discord.Embed(
            title="Queue",
            description=f"{ctx.guild.name}'s music queue.",
            colour=ctx.author.colour,
            timestamp=datetime.utcnow(),
        )

        embed.set_footer(
            text=f"Requested by {ctx.author.display_name}",
            icon_url=ctx.author.avatar_url,
        )

        embed.add_field(
            name="Currently playing",
            value=player.queue.current_track.title,
            inline=False,
        )

        if upcoming := player.queue.upcoming:
            embed.add_field(
                name="Upcoming",
                value="\n".join(t.title for t in upcoming[:show]),
                inline=False,
            )

        await ctx.send(embed=embed)

    @queue_command.error
    async def queue_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("The queue is currently empty.")

    @commands.group(name="volume", invoke_without_command=True, brief="Changes the volume of the music.")
    async def volume_group(self, ctx, volume: int):
        """Changes the volume of the music."""
        player = self.get_player(ctx)

        if volume < 0:
            raise volumeTooLow

        if volume > 150:
            raise volumeTooHigh

        await player.set_volume(volume)
        await ctx.send(f"Volume set to {volume}%")

    @volume_group.error
    async def volume_command_error(self, ctx, exc): 
        if isinstance(exc, volumeTooLow):
            await ctx.send(f"Volume must be between 0% or above.")    
        elif isinstance(exc, volumeTooHigh):
            await ctx.send("The volume must be 150% or below.")

    @volume_group.command(name="up", brief="Increases the volume of the music.")
    async def volume_up_command(self, ctx):
        player = self.get_player(ctx)

        if player.volume == 150:
            raise MaxVolume
        
        await player.set_volume(value := min(player.volume + 10, 150))
        await ctx.send(f"Volume set to {value}%")
    
    @volume_up_command.error
    async def volume_up_command_error(self, ctx, exc): 
        if isinstance(exc, MaxVolume):       
            await ctx.send("The volume is already at maximum.")

    @volume_group.command(name="down", brief="Increases the volume of the music.")
    async def volume_down_command(self, ctx):
        player = self.get_player(ctx)

        if player.volume == 0:
            raise MinVolume
        
        await player.set_volume(value := max(0, player.volume - 10))
        await ctx.send(f"Volume set to {value}%")

    @volume_group.command(name="mute", brief="Mutes the music.")
    async def volume_mute_command(self, ctx):
        player = self.get_player(ctx)

        if player.volume == 0:
            raise MinVolume
        
        await player.set_volume(0)
        await ctx.send(f"Volume set to 0%")

    @volume_mute_command.error
    async def volume_mute_command_error(self, ctx, exc):
        if isinstance(exc, MinVolume):
            await ctx.send("The volume is already at minimum")
    
    @volume_down_command.error
    async def volume_down_command_error(self, ctx, exc): 
        if isinstance(exc, MinVolume):       
            await ctx.send("The volume is already at minimum")


    @commands.command(name="lyrics")
    async def lyrics_command(self, ctx, name: typing.Optional[str]):
        """Searches for a song's lyrics."""
        player = self.get_player(ctx)
        name = name or player.queue.current_track.title

        async with ctx.typing():
            async with aiohttp.request("GET", LYRICS_URL + name, headers={}) as r:
                if not 200 <= r.status <= 299:       
                    raise NoLyricsFound
                
                data = await r.json()

                if len(data["lyrics"]) > 2000:
                    return await ctx.send(f"<{data['links']['genius']}>")

                embed = discord.Embed(title=data["title"], description=data["lyrics"], colour=ctx.author.color, timestamp=datetime.utcnow())

                #embed.set_thumbnail(url=data["thumbnail"])
                embed.set_author(name=data["author"])

                await ctx.send(embed=embed)

    @lyrics_command.error
    async def lyrics_command_error(self, ctx, exc):
        if isinstance(exc, NoLyricsFound):
            await ctx.send("No lyrics found.")

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("music")


def setup(bot):
    bot.add_cog(Music(bot))