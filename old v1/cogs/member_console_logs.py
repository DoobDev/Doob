import discord
from discord.ext import commands

class member_console_logs(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Sends message in console when someone has joined a server with the Doob bot in it
    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'{member} has joined a server with Doob in it.')

    # Sends message in concole when someone has left a server with the Doob bot in it
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member} has left a server with Doob in it.')

def setup(client):
    client.add_cog(member_console_logs(client))