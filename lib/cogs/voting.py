import dbl
import discord
from discord.ext import commands, tasks
import os

import asyncio
import logging

from ..db import db # pylint: disable=relative-beyond-top-level

class voting(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, bot):
        self.bot = bot
        with open("./lib/bot/topgg.txt", "r", encoding="utf-8") as tf:
            TOKEN = tf.read() # set this to your DBL token
        with open ("./lib/bot/webhook.txt", "r", encoding="utf-8") as tf:
            WEBHOOK_AUTH = tf.read()
        self.dblpy = dbl.DBLClient(self.bot, token=TOKEN, webhook_path='/dblwebhook', webhook_auth=WEBHOOK_AUTH, webhook_port=5000) #wtf is this how 2 webhook i dont kow
    
    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        logger.info('Received an upvote')
        print(data)
		#this is the webhook? can you send a test vote pls dont actually vote tho
		#          yeeah i can send test webhook, but idk how 2 webhook  because it be like "webhook_path" and idk wtf that is pls HELP:|
    @commands.Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("voting")

def setup(bot):
    global logger
    logger = logging.getLogger('bot')
    bot.add_cog(voting(bot))