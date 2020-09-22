import dbl
import discord
from discord.ext import commands


class servercount(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, bot):
        self.bot = bot

        with open("./lib/bot/topgg.txt", "r", encoding="utf-8") as tf:
            self.token = tf.read() # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True) # Autopost will post your guild count every 30 minutes
        print("\nTop.gg updated")

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("servercount")

def setup(bot):
    bot.add_cog(servercount(bot))