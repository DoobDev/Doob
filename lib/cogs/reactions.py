from datetime import datetime

from discord import Embed
from discord.ext.commands import Cog

from ..db import db # pylint: disable=relative-beyond-top-level

class Reactions(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.emoji.name == "⭐":
            guild = self.bot.get_guild(payload.guild_id)
            starboardchannel = await self.bot.fetch_channel(db.field("SELECT StarBoardChannel from guilds WHERE GuildID = ?", guild.id))
            message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)

            if not message.author.bot and payload.member.id != message.author.id:
                msg_id, stars = db.record("SELECT StarMessageID, Stars from starboard WHERE (GuildID, MessageID) = (?, ?)", guild.id, message.id) or (None, 0)
                embed = Embed(title=f"⭐ x{stars+1}", colour=message.author.colour, timestamp=datetime.utcnow())

                embed.set_thumbnail(url=message.author.avatar_url)
                embed.set_footer(text=f"⭐ x{stars+1}")

                fields = [("Author", message.author.mention, False),
                        ("Content", message.content or "Image", False)]

                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                if len(message.attachments):
                    embed.set_image(url=message.attachments[0].url)

                if not stars:
                    star_message = await starboardchannel.send(embed=embed)
                    db.execute("INSERT INTO starboard (MessageID, StarMessageID, GuildID) VALUES (?, ?, ?)", message.id, star_message.id, message.guild.id)
                    db.commit()

                else:
                    star_message = await starboardchannel.fetch_message(msg_id)
                    await star_message.edit(embed=embed)
                    db.execute("UPDATE starboard SET Stars = Stars + 1 WHERE (GuildID, MessageID) = (?, ?)", message.guild.id, message.id)
                    db.commit()

            else:
                await message.remove_reaction(payload.emoji, payload.member)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("reactions")

def setup(bot):
    bot.add_cog(Reactions(bot))
