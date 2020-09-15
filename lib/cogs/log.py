from datetime import datetime

from discord import Embed
from discord.ext.commands import Cog, command

from ..db import db # pylint: disable=relative-beyond-top-level

class Log(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("log")

    @Cog.listener()
    async def on_member_update(self, before, after):
        if before.display_name != after.display_name:
            logchannel = await self.bot.fetch_channel(db.field("SELECT LogChannel FROM guilds WHERE GuildID = ?", after.guild.id))
            embed = Embed(title="Member update", description="Nickname has been changed.", colour=after.author.colour, timestamp=datetime.utcnow())

            fields = [("Before", before.display_name, False),
                      ("After", after.display_name, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            embed.set_thumbnail(url=before.author.avatar_url)
            await logchannel.send(embed=embed)
        
        elif before.roles != after.roles:
            embed = Embed(title="Member update", description="Roles has been changed.", colour=after.author.colour, timestamp=datetime.utcnow())
            logchannel = await self.bot.fetch_channel(db.field("SELECT LogChannel FROM guilds WHERE GuildID = ?", after.guild.id))

            fields = [("Before", ", ".join([r.mention for r in before.roles]), False),
                        ("After", ", ".join([r.mention for r in after.roles]), False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            embed.set_thumbnail(url=before.author.avatar_url)
            await logchannel.send(embed=embed)

    @Cog.listener()
    async def on_user_update(self, before, after):
        if before.author.avatar_url != after.avatar_url:
            logchannel = await self.bot.fetch_channel(db.field("SELECT LogChannel FROM guilds WHERE GuildID = ?", after.guild.id))
            embed = Embed(title="Member update", description="Avatar has been changed. BEFORE -->", colour=after.author.colour, timestamp=datetime.utcnow())
            embed.add_field(name="AFTER", value="v (below this)")
            embed.set_thumbnail(url=before.author.avatar_url)
            embed.set_image(url=after.avatar_url) # KEEP THIS AS SET_IMAGE
            await logchannel.send(embed=embed)

        if before.name != after.name:
            logchannel = await self.bot.fetch_channel(db.field("SELECT LogChannel FROM guilds WHERE GuildID = ?", after.guild.id))
            embed = Embed(title="Member update", description="Name has been changed.", colour=after.author.colour, timestamp=datetime.utcnow())

            fields = [("Before", before.name, False),
                      ("After", after.name, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            embed.set_thumbnail(url=before.author.avatar_url)
            await logchannel.send(embed=embed)
        
        if before.discriminator != after.discriminator:
            logchannel = await self.bot.fetch_channel(db.field("SELECT LogChannel FROM guilds WHERE GuildID = ?", after.guild.id))
            embed = Embed(title="Member update", description="Discriminator has been changed.", colour=after.author.colour, timestamp=datetime.utcnow())

            fields = [("Before", before.discriminator, False),
                      ("After", after.discriminator, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            embed.set_thumbnail(url=before.author.avatar_url)
            await logchannel.send(embed=embed)

    @Cog.listener()
    async def on_message_edit(self, before, after):
        if not after.author.bot:
            if before.content != after.content:
                logchannel = await self.bot.fetch_channel(db.field("SELECT LogChannel FROM guilds WHERE GuildID = ?", after.guild.id))
                embed = Embed(title="Message update", colour=after.author.colour, timestamp=datetime.utcnow())

                fields = [("Before", before.content, False),
                        ("After", after.content, False)]

                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                embed.set_thumbnail(url=before.author.avatar_url)
                await logchannel.send(embed=embed)

    # @Cog.listener()
    # async def on_message_delete(self, before, after):
    #     if not after.author.bot:
    #         pass

def setup(bot):
    bot.add_cog(Log(bot))