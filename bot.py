# Doob
import discord
import json
import asyncio
import logging
import os

import aiohttp

from discord.ext import commands

token = input("Copy and paste the Discord Bot Token.\n")

# Creates and loads the json file.
def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix)

client.remove_command("help")

@client.event
async def on_ready():
    print('Doob is online!')
    await client.change_presence(status = discord.Status.online, activity=discord.Game('-help for commands. | github.com/doobdev/doob'))

@client.command()
async def load(ctx, extension):
    print(f'Loaded {extension}')
    client.load_extension(f'cogs.{extension}')
    print(f'Loaded {extension}')

@client.command()
async def unload(ctx, extension):
    print(f'Unloaded {extension}')
    client.unload_extension(f'cogs.{extension}')
    print(f'Unloaded {extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        print(f'Loaded {filename}')

doob_logo = "https://cdn.discordapp.com/avatars/680606346952966177/ada47c5940b5cf8f7e12f61eefecc610.webp?size=1024"

client.run(token)
#hi mr jones lol
