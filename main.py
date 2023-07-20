import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
load_dotenv()

import database

data: dict = database.read()

TOKEN = os.environ['TOKEN']

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'{bot.user} is connected')

@bot.command()
async def hello(ctx):
    await ctx.reply("hello " + ctx.author.name)

#push = 0, pull = 1, leg = 2, rest = 3, skip = 4

import datetime

currentDate = datetime.date.today().strftime("%Y-%m-%d")

@bot.command()
async def start(ctx):
    global data
    username = ctx.author.name
    if data.get(username) == None:
        data[username] = {
            "name": username,
            "history": [],
            "stats" : {
                "bench" : None,
                "squat" : None,
                "deadlift" : None
            },
            "lastUsed": "1900-00-00"
        }
        database.write(data)
        await ctx.reply("Account created " + username)
    else:
        await ctx.reply("Already have an account lil bro " + username)

@bot.command()
async def restart(ctx):
    global data
    username = ctx.author.name
    if username == "imperialeucalyptus" or username == "pugchamp.":
        data[username] = {
            "name": username,
            "history": [],
            "stats" : {
                "bench" : None,
                "squat" : None,
                "deadlift" : None
            },
            "lastUsed": "1900-00-00"
        }
        database.write(data)
        await ctx.reply("Account reset")
    else:
        await ctx.reply("GG")

@bot.command()
async def push(ctx):
    global data
    global currentDate
    username = ctx.author.name
    if data[username] == None:
        await ctx.reply("Please create your profile with !start")
    if data[username]["lastUsed"] == currentDate:
        await ctx.reply("Wait till tomorrow lil bro?")
    else:
        data[username]["history"].append(0)
        data[username]["lastUsed"] = currentDate
        database.write(data)
        await ctx.reply("Push day added.")

@bot.command()
async def pull(ctx):
    global data
    global currentDate
    username = ctx.author.name
    if data[username] == None:
        await ctx.reply("Please create your profile with !start")
    if data[username]["lastUsed"] == currentDate:
        await ctx.reply("Wait till tomorrow lil bro?")
    else:
        data[username]["history"].append(1)
        data[username]["lastUsed"] = currentDate
        database.write(data)
        await ctx.reply("Pull day added.")



@bot.command()
async def leg(ctx):
    global data
    global currentDate
    username = ctx.author.name
    if data[username] == None:
        await ctx.reply("Please create your profile with !start")
    if data[username]["lastUsed"] == currentDate:
        await ctx.reply("Wait till tomorrow lil bro?")
    else:
        data[username]["history"].append(2)
        data[username]["lastUsed"] = currentDate
        database.write(data)
        await ctx.reply("Leg day added.")


@bot.command()
async def rest(ctx):
    global data
    global currentDate
    username = ctx.author.name
    if data[username] == None:
        await ctx.reply("Please create your profile with !start")
    if data[username]["lastUsed"] == currentDate:
        await ctx.reply("Wait till tomorrow lil bro?")
    else:
        data[username]["history"].append(3)
        data[username]["lastUsed"] = currentDate
        database.write(data)
        await ctx.reply("Rest day added.")


@bot.command()
async def skip(ctx):
    global data
    global currentDate
    username = ctx.author.name
    if data[username] == None:
        await ctx.reply("Please create your profile with !start")
    if data[username]["lastUsed"] == currentDate:
        await ctx.reply("Wait till tomorrow lil bro?")
    else:
        data[username]["history"].append(4)
        data[username]["lastUsed"] = currentDate
        database.write(data)
        await ctx.reply("GG you skipped.")


@bot.command()
async def history(ctx, username=None):
    global data
    if username == None:
        username = ctx.author.name
    if data[username] == None:
        await ctx.reply("No history found")
    else:
        totals = [0, 0, 0, 0, 0]
        for e in data[username]["history"]:
            totals[e] += 1
        embed = discord.Embed(title=f"***History - {username}***", color=0x33ffff)
        embed.add_field(name='Push Days: ', value=f'{totals[0]} times', inline=True)
        embed.add_field(name='Pull Days: ', value=f'{totals[1]} times', inline=True)
        embed.add_field(name='Leg Days: ', value=f'{totals[2]} times', inline=True)
        embed.add_field(name='Rest Days: ', value=f'{totals[3]} times', inline=True)
        embed.add_field(name='Skipped: ', value=f'{totals[4]} times', inline=True)
    await ctx.reply(embed=embed)

@bot.command()
async def recent(ctx, username=None):
    global data
    if username == None:
        username = ctx.author.name
    if data[username] == None:
        await ctx.reply("No history found")
    else:
        recent = []
        if len(data[username]["history"]) < 15:
            recent = data[username]["history"]
        else:
            recent = data[username]["history"][-14:]

        embed = discord.Embed(title=f"***Recent - {username}***", color=0xff6666)

        for j in range(len(recent)):
            i = recent[j]
            if i == 0:
                embed.add_field(name=f'Day {j+1}', value="Push 🏋️‍♂️", inline = False)
            elif i == 1:
                embed.add_field(name=f'Day {j+1}', value="Pull 💪", inline = False)
            elif i == 2:
                embed.add_field(name=f'Day {j+1}', value="Leg 🔥", inline = False)
            elif i == 3:
                embed.add_field(name=f'Day {j+1}', value="Rest ✨", inline = False)
            else:
                embed.add_field(name=f'Day {j+1}', value="Skip 💀", inline = False)

    await ctx.reply(embed=embed)

@bot.command()
async def set(ctx, stat, num, unit="lbs"):
    global data
    username = ctx.author.name
    if data.get(username) == None:
        await ctx.reply("Use `!start` to make an account") 
    else:
        if unit == "kg":
            data[username]["stats"][stat] = round(int(num) * 2.2046226218)
        else:
            data[username]["stats"][stat] = int(num)
        database.write(data)
        await ctx.reply(f"Set stat `{stat}` to `{data[username]['stats'][stat]}`")

@bot.command()
async def stats(ctx, user: discord.User=None):
    global data
    data = database.read()
    if user == None:
        user = ctx.author
    if data.get(user.name) == None:
        await ctx.reply("User has no account")
    else:
        s = data.get(user.name)["stats"]
        embed = discord.Embed(
            description="this is the description",
            title="Stats"
        )
        embed.add_field(name="Bench", value=s["bench"])
        embed.add_field(name="Squat", value=s["squat"])
        embed.add_field(name="Deadlift", value=s["squat"])
        await ctx.reply(embed=embed)

@bot.command()
async def date(ctx):
    await ctx.reply(str(datetime.date.today()))

bot.run(TOKEN)
