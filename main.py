import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
load_dotenv()

import database

data = database.read()

TOKEN = os.environ['TOKEN']

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'{bot.user} is connected')

@bot.command()
async def hello(ctx):
    await ctx.reply("hello " + str(ctx.author.name))

@bot.command()
async def start(ctx):
    return

@bot.command()
async def restart(ctx):
    return

@bot.command()
async def push(ctx):
    return

@bot.command()
async def pull(ctx):
    return


@bot.command()
async def leg(ctx):
    return

@bot.command()
async def rest(ctx):
    return

@bot.command()
async def skip(ctx):
    return

@bot.command()
async def history(ctx, name):
    return

bot.run(TOKEN)