#Import Packages
import discord
import os
from flask import Flask
from threading import Thread
import random
from discord.ext import commands

bot = commands.Bot(command_prefix='$')

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


#Startup Sequence

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


#Commands


@client.event
async def on_message(message):
    hello = 'no variable yet!'
    greeting = random.randint(0, 5)
    if greeting == 1:
        hello = 'Hi!'
    if greeting == 2:
        hello = 'Hi There!'
    if greeting == 2:
        hello = 'Hello!'
    if greeting == 3:
        hello = 'Hello There!'
    if greeting == 4:
        hello = 'Hey There!'
    if greeting == 5:
        hello = 'Howdy!'
    if message.author == client.user:
        return
    # each message has a bunch of attributes. Here are a few.
    # check out more by print(dir(message)) for example.
    print(
        f"{message.channel}: {message.author}: {message.author.name}: {message.content}"
    )
    if message.content.startswith('$hello'):
        await message.channel.send(hello)
    if str(message.author) == "Coolpic#0882":
        if 'Who Are You?' in message.content:
            await message.channel.send("I'm you.")
        if 'Get us the link please' in message.content:
            await message.channel.send("Sure thing!")
            await message.channel.send("https://repl.it/join/frkmiakl-coolpic783")
    if "How many people are here?" in message.content:
        GamingAndChill = client.get_guild(653627118248263701)
        await message.channel.send(f"```{GamingAndChill.member_count}```")
        if 'a'

#Run
keep_alive()
token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)
