from discord.ext.commands import Bot as BotBase

PREFIX = "-"
OWNER_IDS = [308000668181069824]

class Bot(BotBase):
    def __init__(self):
        super().__init__(commands_prefix=PREFIX, owner=OWNER_IDS)