import dbl
import discord
from discord.ext import commands
doob_logo = "https://cdn.discordapp.com/avatars/680606346952966177/ada47c5940b5cf8f7e12f61eefecc610.webp?size=1024"

dbltoken = input("Input your Top.gg bot token.\n")

class servercount(commands.Cog):
   # Decorator events.
    def __init__(self, client):
        self.client = client
        self.token = dbltoken # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.client, self.token, autopost=True) # Autopost will post your guild count every 30 minutes
        print("uploaded top.gg")


def setup(client):
    client.add_cog(servercount(client))
