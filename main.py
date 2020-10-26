#Import Packages
import discord,asyncio,youtube_dl
from dotenv import load_dotenv
import discord
from datetime import datetime as d
import os
from flask import Flask
from threading import Thread
import random
from discord.ext import commands
from googleapiclient.discovery import build
from discord.ext.commands import command
import time

def get_prefix(client, message):

    prefixes = ['&', '$']    # sets the prefixes, u can keep it as an array of only 1 item if you need only one prefix

    if not message.guild:
        prefixes = ['$']   # Only allow '==' as a prefix when in DMs, this is optional

    # Allow users to @mention the bot instead of using a prefix when using a command. Also optional
    # Do `return prefixes` if u don't want to allow mentions instead of prefix.
    return commands.when_mentioned_or(*prefixes)(client, message)

bot = commands.Bot(                         # Create a new bot
    command_prefix=get_prefix,              # Set the prefix
    description='A digital manifestation of Coolpic\'s anxiety',  # Set a description for the bot
    owner_id=374886124126208000,            # Your unique User ID
    case_insensitive=True                   # Make the commands case insensitive
)

#Flask Setup

app = Flask('')


@app.route('/')
def home():
    return "I'm alive"


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()

startup_extensions_1 = ["basic", "greeting"]
startup_extensions_2 = ["music","members"]

#Startup Sequence

@bot.event
async def on_ready():
    global GamingAndChill
    GamingAndChill = bot.get_guild(653627118248263701)
    activity = discord.Game(name="With Coolpic's Anxieties")
    await bot.change_presence(status=discord.Status.idle, activity=activity)
    for i in startup_extensions_1:
      bot.load_extension(i)
    for i in startup_extensions_2:
      bot.load_extension(i)
    print('We have logged in as {0.user}'.format(bot))
    return

@bot.command()
async def load(ctx,extension_name : str):
    """Loads an extension."""
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await ctx.send("{} loaded.".format(extension_name))

@bot.command()
async def unload(ctx,extension_name : str):
    """Unloads an extension."""
    bot.unload_extension(extension_name)
    await ctx.send("{} unloaded.".format(extension_name))

@bot.command()
async def add(ctx:str,left : int, right : int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def loop(ctx:str,times : int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)

@bot.command()
async def pages(ctx):
    contents = ["This is page 1!", "This is page 2!", "This is page 3!", "This is page 4!"]
    pages = 4
    cur_page = 1
    message = await ctx.send(f"Page {cur_page}/{pages}:\n{contents[cur_page-1]}")
    # getting the message object for editing and reacting

    await message.add_reaction("◀️")
    await message.add_reaction("▶️")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
        # This makes sure nobody except the command sender can interact with the "menu"

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=60, check=check)
            # waiting for a reaction to be added - times out after x seconds, 60 in this
            # example

            if str(reaction.emoji) == "▶️" and cur_page != pages:
                cur_page += 1
                await message.edit(content=f"Page {cur_page}/{pages}:\n{contents[cur_page-1]}")
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == "◀️" and cur_page > 1:
                cur_page -= 1
                await message.edit(content=f"Page {cur_page}/{pages}:\n{contents[cur_page-1]}")
                await message.remove_reaction(reaction, user)

            else:
                await message.remove_reaction(reaction, user)
                # removes reactions if the user tries to go forward on the last page or
                # backwards on the first page
        except asyncio.TimeoutError:
            await message.delete()
            break
            # ending the loop if user doesn't react after x seconds
@bot.command()
async def slap(ctx, members: commands.Greedy[discord.Member], *, reason='no reason'):
    slapped = ", ".join(x.name for x in members)
    await ctx.send('{} just got slapped because {}'.format(slapped, reason))

#Run
keep_alive()
token = os.environ.get("DISCORD_BOT_SECRET")
bot.run(token)
