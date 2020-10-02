from discord.ext import commands

import statcord


class stat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        with open("./lib/bot/statcord.txt", "r", encoding="utf-8") as tf:
            self.key = tf.read()

        self.api = statcord.Client(self.bot, self.key)
        self.api.start_loop()


    @commands.Cog.listener()
    async def on_command(self,ctx):
        self.api.command_run(ctx)

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("stat")


def setup(bot):
    bot.add_cog(stat(bot))