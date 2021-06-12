from datetime import datetime

from discord import Embed
from discord.ext.commands import Cog

from ..db import db  # pylint: disable=relative-beyond-top-level


class Log(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("log")

    @Cog.listener()
    async def on_member_join(self, member):
        logchannel = await self.bot.fetch_channel(
            db.field("SELECT LogChannel FROM guilds WHERE GuildID = ?", member.guild.id)
        )

        creation_date = member.created_at.strftime("%m/%d/%Y %H:%M;%S")

        globalwarns = db.records(f"SELECT Warns FROM warns WHERE UserID = {member.id}")[
            0
        ][0]

        embed = Embed(
            title="New Member!",
            description=f"{member.display_name} has joined the server!"
            + f"\n\n‣ ID: {member.id}"
            + f"\n‣ Account Creation Date: {creation_date}"
            + f"\n‣ Global Doob Warns: {globalwarns}"
            + f"\n‣ Bot?: {member.bot}",
            colour=0x00D138,
            timestamp=datetime.utcnow(),
        )

        embed.set_thumbnail(url=member.avatar_url)

        await logchannel.send(embed=embed)

    @Cog.listener()
    async def on_member_remove(self, member):
        logchannel = await self.bot.fetch_channel(
            db.field("SELECT LogChannel FROM guilds WHERE GuildID = ?", member.guild.id)
        )

        embed = Embed(
            title="Member Removed.",
            description=f"{member.display_name} has been removed from the server."
            + f"\n\n‣ ID: {member.id}"
            + f"\n‣ Bot?: {member.bot}",
            colour=0xD10003,
            timestamp=datetime.utcnow(),
        )

        embed.set_thumbnail(url=member.avatar_url)

        await logchannel.send(embed=embed)

    @Cog.listener()
    async def on_member_update(self, before, after):
        if before.display_name != after.display_name:
            logchannel = await self.bot.fetch_channel(
                db.field(
                    "SELECT LogChannel FROM guilds WHERE GuildID = ?", after.guild.id
                )
            )
            embed = Embed(
                title="Member update",
                description=f"{before.name}'s Nickname has been changed.",
                colour=after.colour,
                timestamp=datetime.utcnow(),
            )

            fields = [
                ("Before", before.display_name, False),
                ("After", after.display_name, False),
            ]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            embed.set_thumbnail(url=before.avatar_url)
            await logchannel.send(embed=embed)

        elif before.roles != after.roles:
            embed = Embed(
                title="Member update",
                description=f"{before.name}'s Roles has been changed.",
                colour=after.colour,
                timestamp=datetime.utcnow(),
            )
            logchannel = await self.bot.fetch_channel(
                db.field(
                    "SELECT LogChannel FROM guilds WHERE GuildID = ?", after.guild.id
                )
            )

            fields = [
                ("Before", ", ".join([r.mention for r in before.roles]), False),
                ("After", ", ".join([r.mention for r in after.roles]), False),
            ]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            embed.set_thumbnail(url=before.avatar_url)
            await logchannel.send(embed=embed)

    # Currently broken due to me not knowing how to grab the guild id from an on_user_update event, fix coming

    # @Cog.listener()
    # async def on_user_update(self, before, after):
    #     if before.avatar_url != after.avatar_url:
    #         logchannel = await self.bot.fetch_channel(db.field("SELECT LogChannel FROM guilds WHERE GuildID = ?", before.guild.id))
    #         embed = Embed(title=f"{before.name}'s avatar has been changed.'", description="Avatar has been changed. BEFORE -->",  timestamp=datetime.utcnow())
    #         embed.add_field(name="AFTER", value="v (below this)")
    #         embed.set_thumbnail(url=before.avatar_url)
    #         embed.set_image(url=after.avatar_url) # KEEP THIS AS SET_IMAGE
    #         await logchannel.send(embed=embed)

    #     if before.name != after.name:
    #         logchannel = await self.bot.fetch_channel(db.field("SELECT LogChannel FROM guilds WHERE GuildID = ?", before.guild.id))
    #         embed = Embed(title="Member update", description=f"{before.name}'s name has been changed.",  timestamp=datetime.utcnow())

    #         fields = [("Before", before.name, False),
    #                   ("After", after.name, False)]

    #         for name, value, inline in fields:
    #             embed.add_field(name=name, value=value, inline=inline)
    #         embed.set_thumbnail(url=before.author.avatar_url)
    #         await logchannel.send(embed=embed)

    #     if before.discriminator != after.discriminator:
    #         logchannel = await self.bot.fetch_channel(db.field("SELECT LogChannel FROM guilds WHERE GuildID = ?", before.guild.id))
    #         embed = Embed(title="Member update", description=f"{before.name}'s Discriminator has been changed.",  timestamp=datetime.utcnow())

    #         fields = [("Before", before.discriminator, False),
    #                   ("After", after.discriminator, False)]

    #         for name, value, inline in fields:
    #             embed.add_field(name=name, value=value, inline=inline)
    #         embed.set_thumbnail(url=before.author.avatar_url)
    #         await logchannel.send(embed=embed)

    @Cog.listener()
    async def on_message_edit(self, before, after):
        if not after.author.bot:
            if before.content != after.content:
                logchannel = await self.bot.fetch_channel(
                    db.field(
                        "SELECT LogChannel FROM guilds WHERE GuildID = ?",
                        after.guild.id,
                    )
                )
                embed = Embed(
                    title="Message update",
                    description=f"Message from: {after.author.name}",
                    colour=after.author.colour,
                    timestamp=datetime.utcnow(),
                )

                fields = [
                    ("Before", before.content, False),
                    ("After", after.content, False),
                    ("Channel", after.channel, False),
                ]

                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                embed.set_thumbnail(url=before.author.avatar_url)
                await logchannel.send(embed=embed)

    @Cog.listener()
    async def on_message_delete(self, message):
        if not message.author.bot:
            logchannel = await self.bot.fetch_channel(
                db.field(
                    "SELECT LogChannel FROM guilds WHERE GuildID = ?", message.guild.id
                )
            )
            embed = Embed(
                title="Message Deleted",
                description=f"Message from: {message.author.name}",
                colour=message.author.colour,
                timestamp=datetime.utcnow(),
            )

            embed.add_field(name="Message:", value=message.content, inline=False)
            embed.add_field(name="Channel:", value=message.channel, inline=False)
            embed.set_thumbnail(url=message.author.avatar_url)

            await logchannel.send(embed=embed)


def setup(bot):
    bot.add_cog(Log(bot))
