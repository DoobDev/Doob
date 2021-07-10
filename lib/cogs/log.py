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

        globalwarns = db.records(f"SELECT Warns FROM warns WHERE UserID = ?", member.id)[
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

    @Cog.listener()
    async def on_guild_channel_create(self, channel):
        logchannel = await self.bot.fetch_channel(
            db.field(
                "SELECT LogChannel FROM guilds WHERE GuildID = ?", channel.guild.id
            )
        )

        embed = Embed(
            title="New Channel!",
            description=f"Name: {channel.mention}\nCategory: {channel.category}",
            colour=0x00D138,
            timestamp=datetime.utcnow(),
        )

        embed.set_thumbnail(url=channel.guild.icon_url)

        await logchannel.send(embed=embed)

    @Cog.listener()
    async def on_guild_channel_delete(self, channel):
        logchannel = await self.bot.fetch_channel(
            db.field(
                "SELECT LogChannel FROM guilds WHERE GuildID = ?", channel.guild.id
            )
        )

        embed = Embed(
            title="Channel Removed.",
            description=f"Name: {channel.name}\nCategory: {channel.category}",
            colour=0xD10003,
            timestamp=datetime.utcnow(),
        )

        embed.set_thumbnail(url=channel.guild.icon_url)

        await logchannel.send(embed=embed)

    @Cog.listener()
    async def on_guild_channel_update(self, before, after):
        logchannel = await self.bot.fetch_channel(
            db.field("SELECT LogChannel FROM guilds WHERE GuildID = ?", before.guild.id)
        )

        embed = Embed(
            title="Channel Updated", colour=0xFFC31F, timestamp=datetime.utcnow()
        )

        if before.name != after.name:
            embed.add_field(name="Before Name:", value=before.name)
            embed.add_field(name="After Name:", value=after.name)

        if before.category != after.category:
            embed.add_field(name="Before Category:", value=before.category)
            embed.add_field(name="After Category:", value=after.category)

        else:
            embed.add_field(
                name="Something changed, Doob couldn't catch it.",
                value="Check the Audit Log!",
            )

        embed.set_thumbnail(url=before.guild.icon_url)

        await logchannel.send(embed=embed)

    @Cog.listener()
    async def on_guild_role_create(self, role):
        logchannel = await self.bot.fetch_channel(
            db.field("SELECT LogChannel FROM guilds WHERE GuildID = ?", role.guild.id)
        )

        embed = Embed(
            title="New Role!",
            description=f"Name: {role.mention}\nID: {role.id}\nMentionable: {role.mentionable}\nPosition: {role.position}",
            colour=role.colour,
            timestamp=datetime.utcnow(),
        )

        embed.set_thumbnail(url=role.guild.icon_url)

        await logchannel.send(embed=embed)

    @Cog.listener()
    async def on_guild_role_delete(self, role):
        logchannel = await self.bot.fetch_channel(
            db.field("SELECT LogChannel FROM guilds WHERE GuildID = ?", role.guild.id)
        )

        embed = Embed(
            title="Role Deleted.",
            description=f"Name: {role.mention}\nID: {role.id}\nMentionable: {role.mentionable}\nPosition: {role.position}",
            colour=role.colour,
            timestamp=datetime.utcnow(),
        )

        embed.set_thumbnail(url=role.guild.icon_url)

        await logchannel.send(embed=embed)

    @Cog.listener()
    async def on_invite_create(self, invite):
        logchannel = await self.bot.fetch_channel(
            db.field("SELECT LogChannel FROM guilds WHERE GuildID = ?", invite.guild.id)
        )

        embed = Embed(
            title="New Invite!",
            description=f"URL: {invite.url}\nInviter: {invite.inviter}\nMax Age: {invite.max_age}\nMax Uses: {invite.max_uses}",
            colour=0x00D138,
            timestamp=datetime.utcnow(),
        )

        embed.set_thumbnail(url=invite.guild.icon_url)

        await logchannel.send(embed=embed)

    @Cog.listener()
    async def on_invite_delete(self, invite):
        logchannel = await self.bot.fetch_channel(
            db.field("SELECT LogChannel FROM guilds WHERE GuildID = ?", invite.guild.id)
        )

        embed = Embed(
            title="Invite Deleted",
            description=f"URL: {invite.url}\nInviter: {invite.inviter}\nMax Age: {invite.max_age}\nMax Uses: {invite.max_uses}",
            colour=0xD10003,
            timestamp=datetime.utcnow(),
        )

        embed.set_thumbnail(url=invite.guild.icon_url)

        await logchannel.send(embed=embed)

    @Cog.listener()
    async def on_member_ban(self, member):
        logchannel = await self.bot.fetch_channel(
            db.field("SELECT LogChannel FROM guilds WHERE GuildID = ?", member.guild.id)
        )

        embed = Embed(
            title="Member Banned.",
            description=f"{member.display_name} has been banned from the server."
            + f"\n\n‣ ID: {member.id}"
            + f"\n‣ Bot?: {member.bot}",
            colour=0xD10003,
            timestamp=datetime.utcnow(),
        )

        embed.set_thumbnail(url=member.avatar_url)

        await logchannel.send(embed=embed)

    @Cog.listener()
    async def on_member_unban(self, member):
        logchannel = await self.bot.fetch_channel(
            db.field("SELECT LogChannel FROM guilds WHERE GuildID = ?", member.guild.id)
        )

        embed = Embed(
            title="Member Unbanned.",
            description=f"{member.display_name} has been unbanned from the server."
            + f"\n\n‣ ID: {member.id}"
            + f"\n‣ Bot?: {member.bot}",
            colour=0x00D138,
            timestamp=datetime.utcnow(),
        )

        embed.set_thumbnail(url=member.avatar_url)

        await logchannel.send(embed=embed)


def setup(bot):
    bot.add_cog(Log(bot))
