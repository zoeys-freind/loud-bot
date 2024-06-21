import os, sys
import discord
from datetime import datetime
import math
from discord import app_commands
import asyncio, json
import subprocess
from discord.ext import commands
import MemePy
import random
from io import BytesIO
from typing import Union, Optional
from petpetgif import petpet as petpetgif
import base64
import io
import rqst as requests
import urllib
import PIL
from PIL import Image, ImageDraw, ImageFont
import re
import inspect
from threading import Thread
from urllib import parse
import db
from discord.ui import View

os.system("clear")

srcout = sys.stdout

goobuhid = 1014524739059982356

instruct = "You are an AI chatbot integrated into discord through a discord bot named \"Loud Bot\". Respond with very casual messages as if you were a fellow user."

from g4f.client import AsyncClient
from g4f.cookies import set_cookies

set_cookies(".google.com", {"__Secure-1PSID": "g.a000iQijCG0f471f4jZ8hDG4LEMtFt97IHezFhyftv0bqis6n9V-4QCFS21OkWqQxFG2pfdXYwACgYKAbYSAQASFQHGX2Mi920GMyQedcksbVW_LACYQxoVAUF8yKp0tSqxYZRTy7TN5FK-IiHI0076"}) # trashable account.

aiclient = AsyncClient()

async def aigenp(lst):
    sv = json.load(open("./datsv.json", "r"))
    response = await aiclient.chat.completions.create(
        provider=sv["chatprov"],
        model=sv["chatmodel"],
        messages=lst,
        
    )
    return response.choices[0].message.content

async def imggen(prompt):
    response = await aiclient.images.generate(
        model="gemini",
        prompt=prompt,
        
    )
    
    return response.data[0].url
def ginstruct(*fmt):
    instruct.format(*fmt)

async def aigen(message, msd):
    print(msd)
    resp = await aigenp([{'role': 'Instruction', 'content': ginstruct(message.author.name, message.author.display_name)}, *msd])
    return resp

class HttpError(Exception):
    def __init__(self, status_code, message):
        super().__init__(message)

async def stenor(q, i):
    apikey = os.environ["TENORTOKEN"]
    lmt = i
    ckey = "loudbot"
    r = await requests.get(
        "https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=%s&limit=%s" % (parse.quote(q), apikey, ckey,  lmt))

    if r.status_code == 200:
        top_8gifs = r.json()
        return top_8gifs["results"][i-1]["media_formats"]["gif"]["url"]
    else:
        raise HttpError(f"{r.status_code}")

def create_gradient_image(width, height, color1, color2, direction="x"):
    im = Image.new('RGB', (width, height), (255, 255, 255))

    steps = range(0, width if direction == 'x' else height, 1)

    for i in steps:
        ratio = float(i) / len(steps)
        color = tuple([int(c * ratio) for c in color1])
        im.putpixel((i, height // 2), color)

    return im


def hex_to_rgb(hex_color):
    hex_color = str(hex_color)[1:]
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def create_progress_bar(progress, total, length=20):
    # Calculate the number of filled and dotted blocks
    filled_blocks = int(length * progress / total)
    dotted_blocks = length - filled_blocks
    filled_blocks -= 1

    # Create the progress bar string
    progress_bar = "[" + "█" * filled_blocks + "░" * dotted_blocks + "]" + f"{progress-1}%"

    return progress_bar


def error_embed(e):
    embed = discord.Embed(title="Uh oh!", description="An error has occurred.", color=discord.Color.red())
    embed.add_field(name="Details", value=f"Type: {e.__class__.__name__}\nMessage: {e}")
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/1248113218044301353/1248115670202322984/warning-sign-icon-transparent-background-free-png.png?ex=66627dcc&is=66612c4c&hm=d7ec04ee36c2073e9e6fbfc96a201453aefdf5ec76d3ae51c694cd265f4fc6f6&")
    return embed

emptyserver = {"name":"None", "users":{}}

def check_high(user1: discord.User, user2: discord.User):
    return user1.top_role.position > user2.top_role.position



intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.typing = True
intents.guilds = True
intents.messages = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await tree.sync()
    print("Checking data...")
    with open("./checkdata.py", "r") as f:
        exec(f.read(), globals())
    await checkdata()
    print("Ready!")

    datsv = json.load(open("./datsv.json", "r"))
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=getattr(discord.ActivityType, datsv["status"][0]), name=datsv["status"][1]))


for c in os.listdir("./commands"):
    print(f"loading command {c}")
    with open(f"./commands/{c}", "r") as f:
        exec(f.read(), globals())


@client.event
async def on_message(message):
    if message.channel.__class__ != discord.DMChannel:
        if message.author.id == goobuhid and message.content != "":
            q = json.load(open("assets/gquotes.json", "r"))
            q["quotes"].append(message.content)
            json.dump(q, open("assets/gquotes.json", "w"), indent=4)
        srv = db.getserveruser(str(message.guild.id), str(message.author.id))
        if not message.author.bot:
            srv["xp"] += 1
            user_level = srv['level']
            user_xp = srv['xp']
            if user_xp >= (user_level * user_level) + 1:
                srv['level'] += 1
                await message.author.send(embed=discord.Embed(title="You've leveled up!", description=f"Your new level is {srv['level']}.", color=discord.Color.green()))

        db.saveserveruser(str(message.guild.id), str(message.author.id), srv)
        
        if client.user.mention in message.content:
            await message.channel.typing()
            try:
                mssg = await aigen(message, [{"role":message.author.name,"content":message.content}])
                await message.reply(mssg)
            except Exception as e:
                await message.reply(embed=error_embed(e))
    else:
        if not message.reference and message.author.id != client.user.id:
            await message.channel.typing()
            try:
                mssg = await aigen(message, [{"role":message.author.name,"content":message.content}])
                await message.reply(mssg)
            except Exception as e:
                await message.reply(embed=error_embed(e))
        else:
            pass


try:
  token = os.environ["TOKEN"]
  if token == "":
    raise Exception("Please add your token to the Secrets pane.")
  client.run(token)
except discord.HTTPException as e:
    if e.status == 429:
        print(
            "The Discord servers denied the connection for making too many requests"
        )
        print(
            "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests"
        )
    else:
        raise e