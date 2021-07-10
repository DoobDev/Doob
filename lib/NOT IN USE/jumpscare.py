"""
FROM HALLOWEEN 2020
"""
from random import randint

from discord import Member, Embed, Colour
from discord.ext.commands import Cog, command, cooldown, BucketType


class Jumpscare(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="jumpscare", aliases=["js", "scare"], brief="scare friends [temp]")
    async def jumpscare_command(self, ctx, *, target: Member):
        jumpscare = randint(1, 6)

        if jumpscare == 1:
            embed = Embed(
                title="boo",
                description=f"{ctx.author.mention} fnaf jumpscare",
                colour=Colour.red(),
            )
            embed.set_footer(
                text=f"{target.display_name} boo", icon_url=target.avatar_url
            )
            embed.set_image(
                url="https://i.pinimg.com/originals/6d/f2/56/6df256a505c2c0851f0a906c00d7da93.gif"
            )
            await ctx.send(f"{target.mention} lol")
            await ctx.send(embed=embed)

        elif jumpscare == 2:
            embed = Embed(
                title="boo",
                description=f"{ctx.author.mention} fnaf jumpscare",
                colour=Colour.red(),
            )
            embed.set_footer(
                text=f"{target.display_name} boo", icon_url=target.avatar_url
            )
            embed.set_image(
                url="https://i.pinimg.com/originals/ac/fd/40/acfd400be3e5a65503464e395e75947e.gif"
            )
            await ctx.send(f"{target.mention} lol")
            await ctx.send(embed=embed)

        elif jumpscare == 3:
            embed = Embed(
                title="boo",
                description=f"{ctx.author.mention} fnaf jumpscare",
                colour=Colour.red(),
            )
            embed.set_footer(
                text=f"{target.display_name} boo", icon_url=target.avatar_url
            )
            embed.set_image(
                url="https://static.wikia.nocookie.net/fnafapedia/images/e/e4/Fnaf4_jumpscare_chicaindoorway.gif/revision/latest/top-crop/width/220/height/220?cb=20151031010318"
            )
            await ctx.send(f"{target.mention} lol")
            await ctx.send(embed=embed)

        elif jumpscare == 4:
            embed = Embed(
                title="boo",
                description=f"{ctx.author.mention} fnaf jumpscare",
                colour=Colour.red(),
            )
            embed.set_footer(
                text=f"{target.display_name} boo", icon_url=target.avatar_url
            )
            embed.set_image(
                url="https://thumbs.gfycat.com/PertinentSevereKrill-max-1mb.gif"
            )
            await ctx.send(f"{target.mention} lol")
            await ctx.send(embed=embed)

        elif jumpscare == 5:
            embed = Embed(
                title="boo",
                description=f"{ctx.author.mention} fnaf jumpscare",
                colour=Colour.red(),
            )
            embed.set_footer(
                text=f"{target.display_name} boo", icon_url=target.avatar_url
            )
            embed.set_image(url="https://i.makeagif.com/media/7-08-2016/RuqUem.gif")
            await ctx.send(f"{target.mention} lol")
            await ctx.send(embed=embed)

        else:
            embed = Embed(
                title="boo",
                description=f"{ctx.author.mention} fnaf jumpscare",
                colour=Colour.red(),
            )
            embed.set_footer(
                text=f"{target.display_name} boo", icon_url=target.avatar_url
            )
            embed.set_image(
                url="https://thumbs.gfycat.com/ShamelessVainCrossbill-max-1mb.gif"
            )
            await ctx.send(f"{target.mention} lol")
            await ctx.send(embed=embed)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("jumpscare")


def setup(bot):
    bot.add_cog(Jumpscare(bot))
