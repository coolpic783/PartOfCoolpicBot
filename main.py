#Import Packages
import discord
import os
from flask import Flask
from threading import Thread

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
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hi!')


#Run

keep_alive()
token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)
