import discord
from discord.ext.commands import Cog, command, cooldown, BucketType

from discord import Embed
from discord.ext.buttons import Paginator

import re
import math
import random

from ..db import db  # pylint: disable=relative-beyond-top-level

import json

with open("config.json") as config_file:
    config = json.load(config_file)

class Pag(Paginator):
    async def teardown(self):
        try:
            await self.page.clear_reactions()
        except discord.HTTPexception:
            pass
        
class Help(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="help", aliases=["commands"], brief="Shows this help message")
    async def help_command(self, ctx, cog="1"):
        helpEmbed = Embed(title="Help", color=ctx.author.color)
        helpEmbed.set_thumbnail(url=ctx.guild.me.avatar_url)



        cogs = [c for c in self.bot.cogs.keys()]
        # cogs.remove('servercount')
        cogs.remove('Welcome')
        cogs.remove('Reactions')
        cogs.remove('Log')
        # cogs.remove('stat')

        totalPages = math.ceil(len(cogs) / 3 )

        if re.search(f"\d", str(cog)): 
            cog = int(cog)
            if cog > totalPages or cog < 1:
                await ctx.send(f"Invalid argument: `{cog}`\nPlease pick from {totalPages} pages.\nAlternatively, simply run `help` to see page one or type `help [category]` to see that categories help command!")
                return

            helpEmbed.set_footer(text=f"<> - Required, [] - Optional | Page {cog} of {totalPages}")

            neededCogs = []
            for i in range(4):
                x = i + (int(cog) - 1) * 3
                try:
                    neededCogs.append(cogs[x])
                except IndexError:
                    pass

            for cog in neededCogs:
                commandList = "".join(
                    f"`{command.name}` - {command.brief}\n"
                    for command in self.bot.get_cog(cog).walk_commands()
                    if not command.hidden
                )

                commandList += "\n"

                helpEmbed.add_field(name=cog, value=commandList, inline=False)

        elif re.search(r"[a-zA-Z]", str(cog)):
            lowerCogs = [c.lower() for c in cogs]
            if cog.lower() not in lowerCogs:
                await ctx.send(f"Invalid argument: `{cog}`\nPlease pick from {totalPages} pages.\nAlternatively, simply run `help` to see page one or type `help [category]` to see that categories help command!")
                return
            
            helpEmbed.set_footer(text=f"<> - Required, [] - Optional | Cog {(lowerCogs.index(cog.lower())+1)} of {len(lowerCogs)}")

            helpText = ""

            for command in self.bot.get_cog(cogs[lowerCogs.index(cog.lower())]).walk_commands():
                if command.hidden:
                    continue

                params = [
                    f"[{key}]" if "NoneType" in str(value) else f"<{key}>"
                    for key, value in command.params.items()
                    if key not in ("self", "ctx")
                ]

                params = " ".join(params)
                helpText += f"`{command.name}`\n*{command.brief}*\n"

                if len(command.aliases) > 0:
                    helpText += f"⠀⠀‣ Aliases: `{', '.join(command.aliases)}`"
                
                    helpText += '\n'

                prefix = "d!"
                
                if command.parent is not None:
                    helpText += f'⠀⠀‣ Format: `{prefix}{command.parent.name} {command.name} {params}`\n\n'
                else:
                    helpText += f'⠀⠀‣ Format: `{prefix}{command.name} {params}`\n\n'

            helpEmbed.description = helpText
        else:
            await ctx.send(f"Invalid argument: `{cog}`\nPlease pick from {totalPages} pages.\nAlternatively, simply run `help` to see page one or type `help [category]` to see that categories help command!")

        await ctx.send(embed=helpEmbed)


    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("help")


def setup(bot):
    bot.add_cog(Help(bot))
