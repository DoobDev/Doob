import dbl
import discord
from discord.ext import commands
doob_logo = "http://i.mmatt.pw/bz0i1U0V"

class servercount(commands.Cog):
   # Decorator events.
    def __init__(self, client):
        self.client = client
        self.token = 'token' # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.client, self.token, autopost=True) # Autopost will post your guild count every 30 minutes
        print("uploaded top.gg")


def setup(client):
    client.add_cog(servercount(client))
