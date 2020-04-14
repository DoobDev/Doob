import discord
from discord.ext import commands

class startup(commands.Cog):
    def __init__(self, client):
        self.client = client
    # Rotates between the 2 statuses.
#    async def status_task(self, client, asyncio):
#        while True:
#           await asyncio.sleep(10)
#           await client.change_presence(status = discord.Status.online, activity=discord.Game('Thanks for using Doob! | gitlab.com/mmatt625/doob'))
#           await asyncio.sleep(10)
#           await client.change_presence(status = discord.Status.online, activity=discord.Game('Running on Doob v1.06'))
#           await asyncio.sleep(10)

    # Prints in console when the bot is online.
    @commands.Cog.listener()
    async def on_ready(self, client, status_task):
        await client.change_presence(status = discord.Status.online, activity=discord.Game('-help for commands. | gitlab.com/mmatt625/doob'))

#        client.loop.create_tast(status_task()), client, status_task
        print('Doob is online!')

def setup(client):
    client.add_cog(startup(client))
