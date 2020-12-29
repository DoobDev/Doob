from discord.ext import commands

import statcord

import os
from dotenv import load_dotenv

load_dotenv()


class stat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.api = statcord.Client(self.bot, os.environ.get("stat"))
        self.api.start_loop()

    @commands.Cog.listener()
    async def on_command(self, ctx):
        self.api.command_run(ctx)

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("stat")


def setup(bot):
    bot.add_cog(stat(bot))
