from discord import Embed
import asyncio
from discord.ext.commands import Cog, command
import re
import math
from discord_components import Button, ButtonStyle, InteractionType

import re
import math

import json

with open("config.json") as config_file:
    config = json.load(config_file)



class Help(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="help", aliases=["commands"], brief="Shows this help message")
    async def help_command(self, ctx, cog="1"):
        helpEmbed = Embed(title="Help", color=ctx.author.color)
        helpEmbed.set_thumbnail(url=ctx.guild.me.avatar_url)

        cogs = [c for c in self.bot.cogs.keys()]
        cogs.remove('servercount')
        cogs.remove("Welcome")
        cogs.remove("Reactions")
        cogs.remove("Log")
        cogs.remove('stat')

        totalPages = math.ceil(len(cogs) / 4)

        if re.search(f"\d", str(cog)):
            while True:
                cog = int(cog)
                if cog > totalPages or cog < 1:
                    await ctx.send(
                        f"Invalid argument: `{cog}`\nPlease pick from {totalPages} pages.\nAlternatively, simply run `help` to see page one or type `help [category]` to see that categories help command!"
                    )
                    return

                helpEmbed.set_footer(
                    text=f"<> - Required, [] - Optional | Page {cog} of {totalPages} | use `d!help (page number)` to flip pages."
                )

                neededCogs = []
                for i in range(4):
                    x = i + (int(cog) - 1) * 4
                    try:
                        neededCogs.append(cogs[x])
                    except IndexError:
                        pass

                for cog2 in neededCogs:
                    commandList = "".join(
                        f"`{command.name}` - {command.brief}\n"
                        for command in self.bot.get_cog(cog2).walk_commands()
                        if not command.hidden
                    )

                    commandList += "\n"

                    helpEmbed.add_field(name=cog2, value=commandList, inline=False)

                await ctx.send(
                    embed=helpEmbed
                )

        elif re.search(r"[a-zA-Z]", str(cog)):
            lowerCogs = [c.lower() for c in cogs]
            if cog.lower() not in lowerCogs:
                await ctx.send(
                    f"Invalid argument: `{cog}`\nPlease pick from {totalPages} pages.\nAlternatively, simply run `help` to see page one or type `help [category]` to see that categories help command!"
                )
                return

            helpEmbed.set_footer(
                text=f"<> - Required, [] - Optional | Cog {(lowerCogs.index(cog.lower())+1)} of {len(lowerCogs)}"
            )

            helpText = ""

            for command in self.bot.get_cog(
                cogs[lowerCogs.index(cog.lower())]
            ).walk_commands():
                if command.hidden:
                    continue

                params = [
                    f"[{key}]" if "NoneType" in str(value) else f"<{key}>"
                    for key, value in command.params.items()
                    if key not in ("self", "ctx")
                ]

                params = " ".join(params)
                helpText += f"**{command.name}**\n{command.brief}\n"

                if len(command.aliases) > 0:
                    helpText += f"⠀‣ Aliases: `{', '.join(command.aliases)}`"

                    helpText += "\n"

                prefix = "d!"

                if command.parent is not None:
                    helpText += f"⠀‣ Format: `{prefix}{command.parent.name} {command.name} {params}`\n\n"
                else:
                    helpText += f"⠀‣ Format: `{prefix}{command.name} {params}`\n\n"

            helpEmbed.description = helpText
            await ctx.send(embed=helpEmbed)
        else:
            await ctx.send(
                f"Invalid argument: `{cog}`\nPlease pick from {totalPages} pages.\nAlternatively, simply run `help` to see page one or type `help [category]` to see that categories help command!"
            )

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("help")


def setup(bot):
    bot.add_cog(Help(bot))
