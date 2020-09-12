import discord
from discord.ext import commands
import json
import os

f = open('teams.json')
data = json.load(f)
client =  commands.Bot(command_prefix = '.')
client.remove_command('help')

@client.command()
async def help(ctx):
    await ctx.send(
"""Welcome to MS-Teams auto join
We attend meetings for you
- .join {Team} {Time} > Joins the meeting of the specific team
- .teams > Views all the teams in teams.json

Configure your teams.json carefully
    
""")

@client.event
async def on_ready():
    print("--Bot is ready--")

@client.command()
async def hello(ctx):
    await ctx.send(f"Hii {ctx.message.author}")

@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)


@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")


@client.command()
async def r(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")
    print("Reload")

for filename in os.listdir("./cogs"):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(data['bot']['token'])
