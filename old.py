import os, sys
import discord, datetime
import math
import JoveDB
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

os.system("clear")

srcout = sys.stdout

goobuhid = 1014524739059982356
runupdate = True


instruct = "You are an AI chatbot integrated into discord through a discord bot named \"Loud Bot\". Respond with very casual messages as if you were a fellow user."

from g4f.client import AsyncClient
from g4f.cookies import set_cookies

set_cookies(".google.com", {"__Secure-1PSID": "g.a000iQijCG0f471f4jZ8hDG4LEMtFt97IHezFhyftv0bqis6n9V-4QCFS21OkWqQxFG2pfdXYwACgYKAbYSAQASFQHGX2Mi920GMyQedcksbVW_LACYQxoVAUF8yKp0tSqxYZRTy7TN5FK-IiHI0076"})
set_cookies(".bing.com", {"_U":"1qPZSrY1ZZNQej78ECToKBkOqnqOa6qUFB3qizrwMcQQl09We-do1uTMFlpRo0rAK3OdhEiotORoAkvII7e-lCf9s0EggQmvDzXE6774Sc4OBdxZuBfdZs7u-I0z6Oh9N1mcQgS077ImGRbMggtSHcOnbMhfLPTzFTPl5-hkfuROKmWqCks1S5dHggJnvmO6IWqbYyiVCmIcVBdTxNRRIPg"})

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
    if message.guild:
        msd.insert(0, {"role":"Server-specific emojis","content":" ".join("<:"+emj.name+":"+str(emj.id)+">" for emj in message.guild.emojis)})
    print(msd)
    resp = await aigenp([{'role': 'Instruction', 'content': ginstruct(message.author.name, message.author.display_name)}, *msd])
    return resp



async def stenor(q):
    apikey = "AIzaSyCwtT47JtjA-se7DdjJ0K9nxFiqhmqWlOU"
    lmt = 1
    ckey = "loudbot"
    r = await requests.get(
        "https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=%s&limit=%s" % (parse.quote(q), apikey, ckey,  lmt))

    if r.status_code == 200:
        top_8gifs = r.json()
        return top_8gifs["results"][0]["url"]
    else:
        return f"Could not fetch GIF. ({r.status_code})"




# console style
bold = '\033[1m'
italic = '\033[3m'
reset = '\033[0m'
cyan = '\033[36m'
red = '\033[31m'
green = '\033[32m'
yellow = '\033[33m'

def reprint(text, end="\n", type=None, begin=""):
    print(begin+text+reset, end=end)

def get_season():
    return "spring"


def png_to_url(filedata: bytes, filename: str):
    buildurl = "data:image/png;base64,"
    return buildurl + base64.b64encode(filedata).decode()


def extract_text(input_string):
    pattern = r'<@(.*?)>'
    matches = re.findall(pattern, input_string)

    return matches


months = [
    "January", "February", "March", "April", "May", "June", "July", "August",
    "September", "October", "November", "December"
]


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


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.typing = True
intents.guilds = True
intents.messages = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
# --server--
def rgb_to_consolecolor(r, g, b):
    return f'\033[38;2;{r};{g};{b}m'
class err(Exception):
    pass


allowed_roles = ["Moderator", "Administrator", "developers", "server king"]

loudguild = 1088724588369821736
loud2guild = 1150184836569497690
datsttg = False

freindlist = ["1014524739059982356"]

@client.event
async def on_friend_request(request):
    if request.user.id in freindlist:
        await request.accept()
        print(f"Accepted friend request from {request.user.name}")

@client.event
async def on_ready():
    sv = json.load(open("./datsv.json", "r"))
    activity = sv["activity"].lower()
    allowdbegin = ["watching", "playing", "listening", "streaming"]
    if activity.startswith("watching") or activity.startswith(
            "playing") or activity.startswith("listening to") or activity.startswith("streaming"):
        text = activity.replace("watching ", "").replace("playing ", "").replace("listening to ", "").replace("streaming ", "")
        # get attr
        active = getattr(discord.ActivityType, activity.split(" ")[0])
        activ = discord.Activity(type=active, name=text)
        await client.change_presence(status=discord.Status.online, activity=activ)
    
    # sync globally
    await tree.sync()
    print("Ready!")
    if (datsttg):
        for guild in client.guilds:
            jrt = json.load(open("db.json", "r"))
            if guild.id not in jrt:
                jrt["serverdata"][guild.id] = {"warns": {}}
            json.dump(jrt, open("db.json", "w"))
            await on_guildjoin(guild)

    print('Bot has been activated under the name {0.user}'.format(client))
    await updateloop()


async def updateloop():
    print("Checking data...")
    print("Checking servers...")
    await setalser()
    print("Data check done!")


@client.event
async def on_member_join(member):
    guild = member.guild
    dba = JoveDB.load(guild.id)
    if not member.bot:
        dba[str(member.id)] = {}
        usrind = dba[str(member.id)]
        try:
            un = dba[str(member.id)]["level"]
        except:
            dba[member.id] = {
                "level": 0,
                "warns": [],
                "username": member.name,
                "xp": 0,
                "mod": False,
                "admin": False
            }
    print(JoveDB.save(dba))


@client.event
async def on_guild_join(guild):
    await on_guildjoin(guild)
async def on_guildjoin(guild):
    general = discord.utils.get(guild.text_channels, name="general")
    if general and general.permissions_for(guild.me).send_messages:
        await general.send(
            f"Hello, {guild.name}! The bot is setting up your server, and commands will arrive soon. Please wait."
        )
    svrdta = JoveDB.loadserver(guild.id)
    mdt = {}
    mdt["name"] = guild.name
    mdt["id"] = guild.id
    mdt["users"] = {}
    mdt["bl"] = []

    for mbr in guild.members:
        mdt["users"][str(mbr.id)] = {}
        mbs = mdt["users"][str(mbr.id)]

        mbs["username"] = mbr.name
        mbs["xp"] = 0
        mbs["level"] = 0
        mbs["warns"] = []
        mbs["mod"] = False
        mbs["admin"] = False

    JoveDB.saveserver(mdt, guild.id)

    await tree.sync(guild=discord.Object(id=guild.id))
    if general and general.permissions_for(guild.me).send_messages:
        await general.send(
            f"The bot is set up and commands should be activated for your server. Enjoy! :D\n\n### tip:\n- use /help for a list of commands you may use."
        )
        



def check_high(user1: discord.User, user2: discord.User):
    return user1.top_role.position > user2.top_role.position


@client.event
async def on_member_update(before, after):
    if before.bot:
        return
    elif before.roles != after.roles:
        josdb = JoveDB.loadserver(after.guild.id)
        uasr = JoveDB.load(after.guild.id)
        modrole = after.guild.get_role(int(josdb["modrole"]))
        adminrole = after.guild.get_role(int(josdb["adminrole"]))
        if modrole in after.roles and modrole not in before.roles:
            uasr[str(after.id)]["mod"] = True
        elif adminrole in after.roles and adminrole not in before.roles:
            uasr[str(after.id)]["admin"] = True
        elif modrole in before.roles and modrole not in after.roles:
            uasr[str(after.id)]["mod"] = False
        elif adminrole in before.roles and adminrole not in after.roles:
            uasr[str(after.id)]["admin"] = False
        JoveDB.save(uasr, after.guild.id)


def checkperms(level, guild, user):
    if guild:
        if level == "mod":
            usrjsn = JoveDB.load(guild.id)[str(user.id)]
  
            if usrjsn["admin"] or usrjsn["mod"] or user.id == guild.owner.id:
                return True
            else:
                return False
        elif level == "admin":
            usrjsn = JoveDB.load(guild.id)[str(user.id)]
  
            if usrjsn["admin"] or user.id == guild.owner.id:
                return True
            else:
                return False
        elif level == "owner":
            usrjsn = JoveDB.load(guild.id)[str(user.id)]
  
            if user.id == guild.owner.id:
                return True
            else:
                return False
    else:
        return True


# slash commands
"""mod+ template

@tree.command(name = "name", description = "desc")
async def name(interaction):
  if checkperms("mod", interaction.guild, interaction.user)
    pass
  else:
          await interaction.response.send_message("You do not have permission to use this command. Missing permissions 'Moderator' or 'Administrator' or 'Owner'.")

__________________________________________


admin+ template

@tree.command(name = "name", description = "desc")
async def name(interaction):
  if checkperms("admin", interaction.guild, interaction.user)
    pass
  else:
          await interaction.response.send_message("You do not have permission to use this command. Missing permissions 'Administrator' or 'Owner'.")


_____________________________________________



owner+ template

@tree.command(name = "name", description = "desc")
async def name(interaction):
  if checkperms("owner", interaction.guild, interaction.user)
    pass
  else:
          await interaction.response.send_message("You do not have permission to use this command. Missing permissions 'Owner'.")




_________________________________________



everyone template

@tree.command(name = "name", description = "desc")
async def name(interaction):
  pass"""

import time

wait = time.sleep

async def setalser():
    data = JoveDB.loadfile()
    guilds = data["serverdata"]
    for guild in guilds:
        dict1 = guilds[guild]
        template = {
            "name": dict1.get("name", ""),
            "id": dict1.get("id", 0),
            "users": dict1.get("users", {}),
            "bl": dict1.get("bl", []),
            "config": {
                "prefix": "g!",
                "modrole": None,
                "adminrole": None,
                "color": "#000000"
            }
        }
        try:
            if template["name"] == "":
                template["name"] = (await client.fetch_guild(guild)).name
            if template["id"] == 0:
                template["name"] = int((await client.fetch_guild(guild)).id)
            if template["users"] == {}:
                for x in ((await client.fetch_guild(guild))).members:
                    template["users"][str(x.id)] = {"username": x.name, "xp": 0, "level": 0, "warns": [], "admin": False, "mod": False}
        except discord.errors.NotFound:
            pass
                

        dict1.update(template)
        try:
            guilds[guild].update(dict1)
        except:
            pass
    data["serverdata"].update(guilds)
    JoveDB.savefile(data)


async def setalusr(serverID: int):
    # set all users (meant for adding new parameters to the json, like setalser, but users instead of servers.)
    data = JoveDB.loadserver(serverID)
    users = data["users"]
    print(users)
    for user in users:
        dict1 = users[user]
        try:
            template = {
                "username": dict1["username"],
                "xp": dict1["xp"],
                "level": dict1["level"],
                "warns": dict1["warns"],
                "admin": False,
                "mod": False
            }
        except KeyError:
            continue
        dict1.update(template)
        users[user] = dict1
        print(dict1)
    data["users"].update(users)
    print(data)
    JoveDB.saveserver(data, serverID)

class emptyserver:
    members=[]
    name="None"


@tree.command(name="cat", description="Gets a random cat image from thecatapi.")
async def cat(interaction):
    r = await requests.get("https://api.thecatapi.com/v1/images/search")

    await interaction.response.send_message(r.json()[0]["url"])

@tree.command(name = "avatar", description = "Sends a user's avatar.")
async def name(interaction, user:discord.Member|discord.User):
    await interaction.response.send_message(str(user.avatar))


@tree.command(name = "ai-image", description = "Generates an AI image from a provided prompt.")
async def name(interaction, prompt:str):
  await interaction.response.send_message("Generating...")
  msg = await interaction.original_response()
  try:
    res = await imggen(prompt)
    await msg.edit(content=res)
  except Exception as e:
    await msg.edit(content=f"Failed to generate! ({e})")

@tree.command(name = "edit-message", description = "edits a Loud Bot message. Admin+")
@app_commands.describe(mode='How it will be edited.')
@app_commands.choices(mode=[
    app_commands.Choice(name="prepend",value="p"),
    app_commands.Choice(name="append",value="a"),
    app_commands.Choice(name="replace",value="r"),
])
async def name(interaction, message_id:str, content:str, mode:app_commands.Choice[str], newline:bool=True):
  usrjsn = None
  try:
      usrjsn = JoveDB.load(interaction.guild.id)[str(interaction.user.id)]
  except:
      pass
  
  if (interaction.guild == None) or usrjsn["admin"] or interaction.user.id == interaction.guild.owner.id:
    mssg = None
    try:
        mssg = await interaction.channel.fetch_message(message_id)
    except:
        await interaction.response.send_message("Could not fetch message.", ephemeral=True)
    else:
      try:
        if mode.value == "p":
            await mssg.edit(content=content+("\n" if newline else "")+mssg.content)
            await interaction.response.send_message("Edited successfully!", ephemeral=True)
        elif mode.value == "a":
            await mssg.edit(content=mssg.content+("\n" if newline else "")+content)
            await interaction.response.send_message("Edited successfully!", ephemeral=True)
        elif mode.value == "r":
            await mssg.edit(content=content)
            await interaction.response.send_message("Edited successfully!", ephemeral=True)
        else:
            await interaction.response.send_message("Invalid mode.", ephemeral=True)
      except:
          await interaction.response.send_message("Could not edit message.", ephemeral=True)
        
  else:
          await interaction.response.send_message("You do not have permission to use this command. Missing permissions 'Administrator' or 'Owner'.")

@tree.command(name = "tenor", description = "gets the first tenor gif from a search query")
async def name(interaction, search:str):
  res = await stenor(search)
  await interaction.response.send_message(res)


@tree.command(name = "servers", description = "shows the top 3 servers that loud bot is in")
async def name(interaction):
  s = client.guilds
  svrs = [emptyserver, emptyserver, emptyserver]
  for x in s:
      if len(x.members) > len(svrs[2].members):
          svrs.insert(2, x)
      if len(x.members) > len(svrs[1].members):
          svrs.insert(1, x)
      if len(x.members) > len(svrs[0].members):
          svrs.insert(0, x)
  mbed = discord.Embed(title="Top 3 loud bot servers:")
  mbed.add_field(name=f"1. {svrs[0].name}", value=f"{len(svrs[0].members)} members")
  mbed.add_field(name=f"2. {svrs[1].name}", value=f"{len(svrs[1].members)} members")
  mbed.add_field(name=f"3. {svrs[2].name}", value=f"{len(svrs[2].members)} members")
  
  mbed.set_thumbnail(url='https://media.discordapp.net/attachments/1128128913013485618/1235930140060680252/transitions-kinemaster.gif?ex=66362923&is=6634d7a3&hm=2a316cf0b322a62c5236fcc2b9f41f17e2bdbf9fca7f4f0e1d0e222bb964d8d2&')
  
  await interaction.response.send_message(embed=mbed)
  



@tree.command(
    name="edit-permissions",
    description="Allows you to edit a user's mod/admin permission. Admin+")
async def admin_add(interaction,
                    user: discord.User,
                    admin: bool = None,
                    mod: bool = None):
    usrjsn = JoveDB.load(interaction.guild.id)[str(interaction.user.id)]

    if usrjsn["admin"] or interaction.user.id == interaction.guild.owner.id:
        if check_high(
                interaction.user,
                user) or interaction.user.id == interaction.guild.owner.id:
            usrjsn["admin"] = admin
            usrjsn["mod"] = mod
            asb = JoveDB.load(interaction.guild.id)
            asb[str(user.id)].update(usrjsn)
            JoveDB.save(asb, interaction.guild.id)
            await interaction.response.send_message(
                f"Successfully set {user.name}'s admin/mod permission to {admin} and {mod}."
            )

        else:
            await interaction.response.send_message(
                f"You cannot edit someone's permissions if they are higher than you. ({user.top_role.name} > {interaction.user.top_role.name})"
            )

    else:
        await interaction.response.send_message(
            "You do not have permission to use this command. Missing permissions 'Administrator' or 'Owner'."
        )


@tree.command(
    name="config-server",
    description="Allows you to configure the bot for your server. Admin+")
async def config_server(interaction,
                        prefix: str = None,
                        modrole: discord.Role = None,
                        adminrole: discord.Role = None,
                        color: str = None):
    usrjsn = JoveDB.load(interaction.guild.id)[str(interaction.user.id)]

    if usrjsn["admin"] or interaction.user.id == interaction.guild.owner.id:
        data = JoveDB.loadserver(interaction.guild.id)
        if prefix:
            data["config"]["prefix"] = prefix
        if modrole:
            data["config"]["modrole"] = modrole.id
        if adminrole:
            data["config"]["adminrole"] = adminrole.id
        if color:
            data["config"]["color"] = color

        JoveDB.saveserver(data, interaction.guild.id)
        await interaction.response.send_message(
            "The server's configuration has been updated.")
        svrjsn = JoveDB.loadserver(interaction.guild.id)
        for x in interaction.guild.get_role(int(
                svrjsn["config"]["adminrole"])).members:
            usrjsn2 = JoveDB.load(interaction.guild.id)[str(x.id)]
            usrjsn2["admin"] = True
            usrjsn2["mod"] = True
            JoveDB.save(usrjsn2, interaction.guild.id)
        for x in interaction.guild.get_role(int(
                svrjsn["config"]["modrole"])).members:
            usrjsn2 = JoveDB.load(interaction.guild.id)[str(x.id)]
            usrjsn2["mod"] = True
            JoveDB.save(usrjsn2, interaction.guild.id)
    else:
        await interaction.response.send_message(
            "You do not have permission to use this command. Missing permissions 'Administrator' or 'Owner'."
        )


@tree.command(name="change-activity",
              description="Changes the bot's activity.")
async def change_activity(interaction, activity: str):
    bact = activity
    activity = activity.lower()
    
    allowdbegin = ["watching", "playing", "listening", "streaming"]
    # check if the activity arg begins woth anything in the list
    if activity.startswith("watching") or activity.startswith(
            "playing") or activity.startswith(
                "listening to") or activity.startswith("streaming"):
        text = bact.replace("watching ",
                                "").replace("playing ", "").replace(
                                    "listening to ",
                                    "").replace("streaming ", "")
        # get attr
        active = getattr(discord.ActivityType, activity.split(" ")[0])
        activ = discord.Activity(type=active, name=text)
        await client.change_presence(status=discord.Status.online,
                                     activity=activ)
        sv = json.load(open("./datsv.json", "r"))
        sv["activity"] = activity
        json.dump(sv, open("./datsv.json", "w"))
        await interaction.response.send_message("Activity set!",
                                                ephemeral=True)
    else:
        await interaction.response.send_message(
            "Invalid activity type. please begin your activity with: watching, playing, listening to, streaming",
            ephemeral=True)



@tree.command(name="quote", description="Quotes a message (by ID)")
async def quote(interaction, message_id: str):
    message = await interaction.channel.fetch_message(message_id)
    gradient = Image.open("New Project.png")
    gradient = gradient.convert("RGBA")

    # Open an image file
    req = await requests.get(str(message.author.avatar))

    image = Image.open(BytesIO(req.content))
    image = image.convert("RGBA")
    bg = Image.new("RGBA", (1080, 750), "white")
    image = image.resize((1080, 1080))

    # Create a mask from the alpha channel of the gradient
    mask = gradient.split()[3]

    # Paste the gradient onto the background using the mask

    bg.paste(image, (0, -270))

    bg.paste(gradient, (0, 0), mask)
    font = ImageFont.truetype("DejaVuSansMono-Bold.ttf", size=40)
    draw = ImageDraw.Draw(bg)

    # wrap text with newlines.
    wrappable = message.content
    final = ""
    indx = 0
    for x in wrappable.split(" "):
        final += x + " "
        if indx >= 4 or len(x) > 10:
            final += "\n"
            indx = 0
        indx += 1

    for x in extract_text(wrappable):
        name = interaction.guild.get_member(int(x)).name
        wrappable = wrappable.replace(f"<@{x}>", f"@{name}")
    # wrapped white text on image

    draw.text((50, 50), final, font=font, fill=(255, 255, 255, 255))
    draw.text((350, 650),
              f"- {message.author.name}, {datetime.datetime.now().year}",
              font=font,
              fill=(255, 255, 255, 255))

    barr = BytesIO()
    bg.save(barr, format="PNG")
    barr.name="quote.png"
    barr.seek(0)

    await interaction.response.send_message(file=discord.File(barr))


@tree.command(name="shutdown", description="Turns off the bot. Dev+")
async def shutdown(interaction, reason: str = "no reason given"):
    if str(interaction.user.id) == str(goobuhid):
        await interaction.response.send_message(
            f"Shutting down... <@{goobuhid}>\nReason: \"{reason}\""
        )
        exit()
    else:
        await interaction.response.send_message(
            "You do not have permission to use this command."
        )


@tree.command(name="addemoji", description="creates an emoji. mod+")
async def addemoji(interaction, name: str, image_url: str):
    usrjsn = JoveDB.load(interaction.guild.id)[str(interaction.user.id)]

    if usrjsn["admin"] or usrjsn[
            "mod"] or interaction.user.id == interaction.guild.owner.id:
        # Fetch the image
        imgbytes = (await requests.get(image_url)).content
        imgbytes = base64.b64decode(imgbytes)
        imgbytes = BytesIO(imgbytes).read()
        new_emoji = await interaction.guild.create_custom_emoji(name=name,
                                                                image=imgbytes)

        await interaction.response.send_message(
            f"Emoji {new_emoji.name} created: {new_emoji}", ephemeral=True)
    else:
        await interaction.response.send_message(
            "You do not have permission to use this command. Missing permissions 'Moderator' or 'Administrator' or 'Owner'."
        )


@tree.command(name="profile", description="sends your profile card.")
async def profile(interaction,
                  user: discord.Member = None,
                  config: bool = False):
    if user is None:
        user = interaction.user
    if user.bot == False:
        if not config:
            # (15, 18)
            template = Image.new("RGBA", (780, 350), (20, 20, 60))
            season = "pfdd.png"
            gtemplate = Image.open(season)
            template.paste(gtemplate, (0, 0))
            avatar_url = user.display_avatar.url
            print(avatar_url)
            avatar_data = (await requests.get(avatar_url)).content
            print('gt')

            avatar_image = Image.open(BytesIO(avatar_data))
            avatar_image = avatar_image.resize((300, 300))
            # add background shadow
            shadow = Image.new("RGBA", avatar_image.size, (20, 20, 60, 80))

            template.paste(shadow, (5, 8))
            template.paste(avatar_image, (15, 18))
            # add big text with username
            font = ImageFont.truetype("DejaVuSansMono-Bold.ttf", size=40)
            draw = ImageDraw.Draw(template)
            draw.text((335, 18), user.name, (255, 255, 255), font=font)
            # add small text with level
            usr = JoveDB.load(interaction.guild.id)[str(user.id)]
            if user.top_role.name.endswith("s"):
                tprl = user.top_role.name[:-1]
            else:
                tprl = user.top_role.name
            font = ImageFont.truetype("DejaVuSansMono-Bold.ttf", size=30)
            draw.text((335, 58),
                      tprl,
                      hex_to_rgb(user.top_role.color),
                      font=font)
            font = ImageFont.truetype("DejaVuSansMono.ttf", size=20)

            draw.text(
                (335, 90),
                f"{create_progress_bar(usr['xp']-(usr['level']-1) * (usr['level']-1) + 1, ((usr['level'] * usr['level']) + 1)-(usr['level']-1) * (usr['level']-1) + 1, 30)}\nLevel: {usr['level']}\nXP: {usr['xp']}\n# of warns: {len(usr['warns'])}\nAdmin: {user.top_role.permissions.administrator}\n",
                (255, 255, 255),
                font=font)

            barr = BytesIO()
            template.save(barr, format="PNG")
            barr.name="profile.png"
            barr.seek(0)

            await interaction.response.send_message(file=discord.File(barr))
    else:
        await interaction.response.send_message(
            "You can't use this command on bots.", ephemeral=True)


@tree.command(
    name="backup",
    description=
    "Backs up all user data. Best to use this when /wip doesn't say 'MAKING AN UPDATE'."
)
async def backup(interaction):
    dast = json.load(open("db.json", "r"))
    json.dump(dast, open("dbBackup.json", "w"))
    print(interaction.__class__)
    await interaction.response.send_message("Data backup finished.",
                                            ephemeral=True)


@tree.command(name="wip",
              description="Sends what is currently in progress with the bot.")
async def wip(interaction):
    await interaction.response.send_message(
        """**What is currently in progress?**
  
- reintroducing g! commands.

MAKING AN UPDATE""",
        ephemeral=True)


@tree.command(name="petpet", description="PAT THEM")
async def petpet(ctx, user: discord.member.Member):
    r = BytesIO((await requests.get(str(user.avatar))).content)
    dest = BytesIO()
    petpetgif.make(r, dest)
    dest.seek(0)
    await ctx.response.send_message(file=discord.File(dest, filename=f"{user.name}-petpet.gif"))


@tree.command(name="image-petpet", description="PAT THEM")
async def petpet(ctx, file: discord.Attachment):
    r = BytesIO((await requests.get(file.proxy_url)).content)
    dest = BytesIO()
    petpetgif.make(r, dest)
    dest.seek(0)
    await ctx.response.send_message(file=discord.File(dest, filename=f"petpet.gif"))


@tree.command(name="lb", description="Shows the top 10 users in the server.")
async def leaderboard(interaction):
    dbc = JoveDB.load(interaction.guild.id)
    leaderboard = sorted(dbc.items(),
                         key=lambda x: x[1]['level'],
                         reverse=True)[:10]
    leaderboard_text = "Top 10 Users:\n"
    for i, (user_id, user_data) in enumerate(leaderboard):
        try:
            member = interaction.channel.guild.get_member(int(user_id))
            leaderboard_text += f"{i+1}. {member.name} - Level: {user_data['level']}\n"
        except:
            print("Error")
    await interaction.response.send_message(leaderboard_text)


@tree.command(name="embed", description="Creates an embed.")
async def create_embed(interaction,
                       title: str,
                       desc: str,
                       footer: str = "",
                       url: str = "",
                       image: str = "",
                       thumbnail: str = "",
                       feild_name: str = "",
                       feild_desc: str = ""):
    embed = discord.Embed(timestamp=discord.utils.utcnow())
    embed.set_author(name=interaction.user.name,
                     icon_url=interaction.user.avatar)
    embed.title = title
    embed.description = desc
    if footer != "":
        embed.set_footer(text=footer)
    if url != "":
        embed.url = url

    if image != "":
        embed.set_image(url=image)
    if thumbnail != "":
        embed.set_thumbnail(url=thumbnail)
    if feild_name != "":
        if feild_desc == "":
            feild_desc = "No context given."
        embed.add_field(name=feild_name, value=feild_desc, inline=False)
    await interaction.channel.send(embed=embed)
    await interaction.response.send_message(f"Embed created.", ephemeral=True)


@tree.command(name="loudembed",
              description="creates an update embed. mod+",
              guilds=[discord.Object(id=loudguild)])
async def loudembed(interaction,
                    version: str = "",
                    desc: str = "",
                    type: str = ""):  # u, e, s
    if any(role.name in ["head developers"]
           for role in interaction.user.roles):
        if version == "":
            version = "1.0.0 - UNSET"
        if desc == "":
            desc = "No context provided."
        if type == "u":
            embed = discord.Embed(title="LOUD BOT UPDATE",
                                  description=desc,
                                  color=0x00ff00)
            embed.set_footer(text=f"Version {version}")
        elif type == "e":
            embed = discord.Embed(title="LOUD BOT ERROR REPORT",
                                  description=desc,
                                  color=0xff0000)
        elif type == "s":
            embed = discord.Embed(title="LOUD BOT STATUS REPORT",
                                  description=desc,
                                  color=0xffff00)
        await interaction.response.send_message("Embed sent.", ephemeral=True)
        await client.get_channel(1161164921220911114).send(embed=embed)

    else:
        await interaction.response.send_message(
            "You do not have permission to use this command. Missing permissions 'Administrator' or 'Owner'."
        )


@tree.command(name="py", description="runs python code. admin+")
async def py(interaction, python: str, input: str = ""):
    if checkperms("admin",interaction.guild,interaction.user):
        await interaction.response.send_message("Executing...", ephemeral=True)

        try:
            # Use asyncio to run the subprocess with a timeout of 60 seconds
            result = await asyncio.wait_for(
                asyncio.to_thread(lambda: subprocess.run(
                    ["python", "-c", python],
                    input=input,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )),
                timeout=60,
            )

            if result.stderr:
                await interaction.channel.send("```\n"+result.stderr+"```")
            else:
                rs = result.stdout
                if result.stdout == "":
                    rs = "[ Executed, no output ]"
                await interaction.channel.send(rs)
        except asyncio.TimeoutError:
            await interaction.channel.send("{interaction.user.mention} The command execution timed out (1 minute).")
    else:
        await interaction.response.send_message(
            "You do not have permission to use this command. Missing permissions 'Administrator' or 'Owner'."
        )


@tree.command(name="say", description="Sends text.")
async def say(interaction, message: str, reply_id: str = None):
    if reply_id is None:
        await interaction.channel.send(message)
        await interaction.response.send_message("sent.", ephemeral=True)
    else:
        mesg = await interaction.channel.fetch_message(int(reply_id))
        await mesg.reply(message)
        await interaction.response.send_message(
            f"replied to {mesg.author.name}.", ephemeral=True)
        open("logs.txt", "a").write(f"""
[say]
[user: {interaction.user.name}, content: '{message}'""")
    f = open("saylogs.md", "a")
    f.write(
        f'## {interaction.user.name}:\n"{message}"\n - {datetime.datetime.now().strftime("%I:%M %p - %Y-%m-%d")}\n\n'
    )
    f.close()


@tree.command(name="dm", description="Sends text to a user.")
async def dm(interaction,
             user: discord.Member,
             message: str,
             mass: bool = False):
    if mass is False:
        await user.send(message)
        await interaction.response.send_message("sent.", ephemeral=True)

    else:
        guild: discord.Guild = interaction.guild
        async def loop():
            async for x in guild.fetch_members():
    
                await x.send(message)
            await interaction.response.send_message(
                f"sent to {len(interaction.channel.guild.members)} users.",
                ephemeral=True)
        runner = lambda: asyncio.run(loop())
        Thread(target=runner).start()


@tree.command(name="blacklist",
              description="Adds/removes a word from the blacklist. mod+")
async def blacklist(interaction, word: str, remove: bool):
    usrjsn = JoveDB.load(interaction.guild.id)[str(interaction.user.id)]

    if usrjsn["admin"] or usrjsn[
            "mod"] or interaction.user.id == interaction.guild.owner.id:
        if bool is True:
            dbf = JoveDB.loadserver(interaction.guild.id)
            word = f" {word} "
            if word.lower() not in dbf["bl"]:
                await interaction.response.send_message(
                    "Select word isn't in the blacklist.\n\nblacklist:\n" +
                    str(dbf["bl"]),
                    ephemeral=True)
            else:
                del dbf["bl"][dbf["bl"].index(word.lower())]
                await interaction.response.send_message(
                    "Deleted from blacklist.", ephemeral=True)

        else:
            dbf = JoveDB.loadserver(interaction.guild.id)
            if word.lower() in dbf["bl"]:
                await interaction.response.send_message(
                    "Select word is already in the blacklist.\n\nblacklist:\n"
                    + str(dbf["bl"]),
                    ephemeral=True)
            else:
                dbf["bl"].append(f" {word.lower()} ")

                await interaction.response.send_message("Added to blacklist.",
                                                        ephemeral=True)
        JoveDB.save(dbf)

    else:
        await interaction.response.send_message(
            "You do not have permission to use this command. Missing permissions 'Administrator' or 'Owner'."
        )


@tree.command(name="hi", description="Why not say hi!")
async def hi(interaction):
    await interaction.response.send_message(f'Hello, {interaction.user.name}!')


@tree.command(name="help", description="Sends the help menu.")
async def help(interaction):
    await interaction.response.send_message(
        "Check your DMs. (you may need to turn on your DMs)", ephemeral=True)
    # build help menu
    cmdlist = []
    for x in tree.get_commands():
        cmdlist.append(f"**{x.name}** - {x.description}")

    hlpblt = ""
    for x in cmdlist:
        hlpblt += f"- {x},\n"
    hlpblt = hlpblt[:-2]

    await interaction.user.send(
        embed=discord.Embed(title="Help menu", description=hlpblt))


@tree.command(name="ping", description="Checks the bot's ping.")
async def ping(interaction):
    await interaction.response.send_message(embed=discord.Embed(
        title="Bot latency", description=f'{round(client.latency * 1000)}ms'))


@tree.command(name="kick", description="Kicks the mentioned user. mod+")
async def kick(interaction, user: discord.Member, fake: bool = False):
    usrjsn = JoveDB.load(interaction.guild.id)[str(interaction.user.id)]

    if usrjsn["admin"] or usrjsn[
            "mod"] or interaction.user.id == interaction.guild.owner.id:
        if not fake:
            await interaction.response.send_message(embed=discord.Embed(
                title="/kick", description=f'{user.name} has been kicked.'))
            await user.kick()
        else:
            await interaction.response.send_message(
                f'{user.name} has been kicked.')
    else:
        await interaction.response.send_message(
            "You do not have permission to use this command. Missing permissions 'Administrator' or 'Owner'."
        )


@tree.command(name="ban", description="Bans the mentioned user. mod+")
async def ban(interaction, user: discord.Member, mssg_del_days: int = 0):

    usrjsn = JoveDB.load(interaction.guild.id)[str(interaction.user.id)]

    if usrjsn["admin"] or usrjsn[
            "mod"] or interaction.user.id == interaction.guild.owner.id:
        await user.ban(delete_message_days=mssg_del_days)
        await interaction.response.send_message(f'{user.name} has been banned.'
                                                )
    else:
        await interaction.response.send_message(
            "You do not have permission to use this command. Missing permissions 'Administrator' or 'Owner'."
        )


@tree.command(name="mute", description="Mutes the mentioned user. mod+")
async def mute(interaction, member: discord.Member):
    usrjsn = JoveDB.load(interaction.guild.id)[str(interaction.user.id)]

    if usrjsn["admin"] or usrjsn[
            "mod"] or interaction.user.id == interaction.guild.owner.id:
        role = discord.utils.get(interaction.channel.guild.roles, name="Muted")
        if not role:
            role = await interaction.channel.guild.create_role(name="Muted")
            for channel in interaction.channel.guild.channels:
                await channel.set_permissions(role,
                                              speak=False,
                                              send_messages=False)
        await member.add_roles(role)
        await interaction.response.send_message(
            f"{member.name} has been muted. use /unmute to unmute them.")

    else:
        await interaction.response.send_message(
            "You do not have permission to use this command. Missing permissions 'Administrator' or 'Owner'."
        )


@tree.command(name="unmute", description="Unmutes the mentioned user. mod+")
async def unmute(interaction, user: discord.Member):
    usrjsn = JoveDB.load(interaction.guild.id)[str(interaction.user.id)]

    if usrjsn["admin"] or usrjsn[
            "mod"] or interaction.user.id == interaction.guild.owner.id:
        role = discord.utils.get(interaction.channel.guild.roles, name="Muted")
        if not role:
            role = await interaction.channel.guild.create_role(name="Muted")
            for channel in interaction.channel.guild.channels:
                await channel.set_permissions(role,
                                              speak=False,
                                              send_messages=False)
        await user.remove_roles(role)
        await interaction.response.send_message(
            f'{user.name} has been unmuted.')

    else:
        await interaction.response.send_message(
            "You do not have permission to use this command. Missing permissions 'Administrator' or 'Owner'."
        )


@tree.command(name="warn", description="Warns the mentioned user. mod+")
async def warn(interaction,
               user: discord.Member,
               reason: str = "No reason given."):
    usrjsn = JoveDB.load(interaction.guild.id)[str(interaction.user.id)]

    if usrjsn["admin"] or usrjsn[
            "mod"] or interaction.user.id == interaction.guild.owner.id:
        await interaction.response.send_message(f'{user.name} has been warned.'
                                                )
        dbe = JoveDB.load(interaction.guild.id)
        dbe[str(user.id)]["warns"].append(reason)
        JoveDB.save(dbe, interaction.guild.id)
    else:
        await interaction.response.send_message(
            "You do not have permission to use this command. Missing permissions 'Administrator' or 'Owner'."
        )


@tree.command(name="warns", description="Checks the mentioned user's warns.")
async def warns(interaction, user: discord.Member):
    usrjsn = JoveDB.load(interaction.guild.id)[str(interaction.user.id)]

    if usrjsn["admin"] or usrjsn[
            "mod"] or interaction.user.id == interaction.guild.owner.id:

        dbe = JoveDB.load(interaction.guild.id)
        wrns = ''
        ind = 0
        wrns = str(dbe[str(user.id)]["warns"])
        await interaction.response.send_message(
            f"{user.name}'s warns:\n\n{wrns}\n\nUse /rmwarn to remove a warn.")
    else:
        await interaction.response.send_message(
            "You do not have permission to use this command. Missing permissions 'Administrator' or 'Owner'."
        )


@tree.command(name="unban",
              description="Unbans the user with the given ID. mod+")
async def unban(interaction, user: discord.Member):
    member = user
    usrjsn = JoveDB.load(interaction.guild.id)[str(interaction.user.id)]

    if usrjsn["admin"] or usrjsn[
            "mod"] or interaction.user.id == interaction.guild.owner.id:
        role = discord.utils.get(interaction.channel.guild.roles, name="Muted")
        if not role:
            await interaction.response.send_message(
                "There is no `Muted` role to remove.")
            return
        await member.remove_roles(role)
        await interaction.channel.send(f"{member.name} has been unmuted.")
    else:
        await interaction.response.send_message(
            "You do not have permission to use this command. Missing permissions 'Administrator' or 'Owner'."
        )


@tree.command(name="rank",
              description="replys with the mentioned user's rankings.")
async def rank(interaction, user: discord.Member = None):
    if user is None:
        user = interaction.user
    member = user
    if not member.bot:
        dbb = JoveDB.load(interaction.guild.id)
        level = str(dbb[str(member.id)]["level"])
        xp = str(dbb[str(member.id)]["xp"])
        await interaction.response.send_message(
            f"{member.name}'s level is {level}.\nXP: ({xp} / {int(level) * int(level) + 1})"
        )
    else:
        await interaction.response.send_message("Bots don't have ranks.")


@tree.command(name="setlevel", description="sets your level. mod+")
async def setlevel(interaction, level: int, user: discord.Member = None):
    usrjsn = JoveDB.load(interaction.guild.id)[str(interaction.user.id)]

    if usrjsn["admin"] or usrjsn[
            "mod"] or interaction.user.id == interaction.guild.owner.id:
        if user is None:
            member = interaction.user
        else:
            member = user
        dbc = JoveDB.load(interaction.guild.id)
        dbc[str(member.id)]['level'] = int(level)
        x = dbc[str(member.id)]['level'] - 1
        dbc[str(member.id)]['xp'] = (x * x) + 2
        print(JoveDB.save(dbc))
        await interaction.response.send_message("Your level has been set!")
        leaderboard = sorted(dbc.items(),
                             key=lambda x: x[1]['level'],
                             reverse=True)[:10]
        highest_level_user = leaderboard[0]
        if dbc[str(member.id)]['level'] > highest_level_user[1]["level"]:
            role = discord.utils.get(interaction.channel.guild.roles,
                                     name="1st place")
            await highest_level_user[0].remoe_roles(role)
            await interaction.user.add_roles(role)

    else:
        await interaction.response.send_message(
            "You do not have permission to use this command. Missing permissions 'Administrator' or 'Owner'."
        )


@tree.command(name="rmwarn", description="Removes a warn.")
async def rmwarn(interaction, user: discord.Member, warn: int):
    usrjsn = JoveDB.load(interaction.guild.id)[str(interaction.user.id)]

    if usrjsn["admin"] or usrjsn[
            "mod"] or interaction.user.id == interaction.guild.owner.id:
        dbf = JoveDB.load(interaction.guild.id)
        warnStr = dbf[str(user.id)]["warns"][warn - 1]
        del dbf[str(user.id)]["warns"][warn - 1]
        JoveDB.save(dbf)
        await interaction.response.send_message(
            f"Warn '{warnStr}' has been removed from {user.name}.")
    else:
        await interaction.response.send_message(
            "You do not have permission to use this command. Missing permissions 'Administrator' or 'Owner'."
        )


@tree.command(name="purge",
              description="mass deletes a select amout of messages. mod+")
async def purge(interaction, amount: int = None):
    usrjsn = JoveDB.load(interaction.guild.id)[str(interaction.user.id)]

    if usrjsn["admin"] or usrjsn[
            "mod"] or interaction.user.id == interaction.guild.owner.id:
        if amount is None:
            await interaction.channel.purge()
            await interaction.channel.send(
                f"{interaction.user.name} has purged all messages in #{interaction.channel.name}"
            )
        else:
            await interaction.channel.purge(limit=amount)
            await interaction.channel.send(
                f"{interaction.user.name} has purged {amount} messages in #{interaction.channel.name}"
            )
        await interaction.response.send_message("👍", ephemeral=True)

    else:
        await interaction.response.send_message(
            "You do not have permission to use this command. Missing permissions 'Administrator' or 'Owner'."
        )


async def get_mssg_from_reference(ref: discord.MessageReference,
                                  channel: discord.TextChannel):
    return await channel.fetch_message(ref.message_id)


# g! commands



class MI:
    """
creates a mock interaction that redirects to the message specified.
"""

    class rese():

        def __init__(sef, message):
            sef.message = message

        async def send_message(self, content=None, ephemeral=False, file:discord.File=None):
            if not ephemeral:
                await self.message.reply(content, file=file)
            else:
                await self.message.author.send(content, file=file)

    resle = rese

    def __init__(self, message: discord.Message):
        self.message = message
        self.channel = message.channel
        self.guild = message.guild
        self.response = self.resle(message)
        self.user = message.author

class MessageArchive:
    def __init__(self, mssg):
        self.__origin__ = mssg
        self.content = mssg.content
        self.author = mssg.author
        self.attachments = mssg.attachments
        self.embeds = mssg.embeds
        self.id = mssg.id
        self.channel = mssg.channel
        self.guild = mssg.guild

@client.event
async def on_message(message):
    blocked = []
    for word in blocked:
        if word in message.content.lower() and (
                message.channel.__class__ !=
                discord.DMChannel) and message.author != client.user:
            await message.delete()
            await message.author.send(
                f"You have been auto-warned for using the blocked word \"{word}\". This warn is appealable."
            )
            # add the warn
            usrd = JoveDB.load(message.guild.id)
            usrd[str(message.author.id)]["warns"].append(
                f"Auto-warn: blacklisted word \"{word}\".")
            JoveDB.save(usrd, message.guild.id)
    if message.author == client.user:
        return
    if not message.author.bot:
        if message.channel.__class__ != discord.DMChannel:
            dbd = JoveDB.load(message.guild.id)
            user_id = str(message.author.id)
            user_xp = dbd[user_id]['xp']
            user_level = dbd[user_id]['level']

            # Update the user's XP and level
            dbd[user_id]['xp'] += 1
            if user_xp >= (user_level * user_level) + 1:
                dbd[user_id]['level'] += 1
                await message.author.send(
                    f"You've leveled up! Your new level is {dbd[user_id]['level']}."
                )

            JoveDB.save(dbd, message.guild.id)
            """dbg = JoveDB.load(message.guild.id)
      if any(item in message.content.lower().split(" ") for item in dbg["bl"]):
        await message.author.send("Your message was deleted because it contained a blacklisted word.")
        await message.delete()"""
        if message.content.lower().startswith("g!"):
            cmdnames = [cmd.name for cmd in tree.get_commands()]
            using = message.content.lower().split(" ")[0][2:]
            if using in cmdnames:
                cmd = tree.get_command(using).callback
                args = []
                # generate args
                pers = inspect.signature(cmd).parameters
                perlist = list(pers.values())
                mssgargs = re.findall(r'[^"\s]+|"[^"]*"', message.content)[1:]
                indx = 1
                argtype = None
                if len(pers) > 1:
                    for arga in mssgargs:
                      argname = perlist[indx].name
                      argtype = perlist[indx].annotation
                      try:
                        if argtype == str:
                            args.append(arga)
                        elif argtype == int:
                            args.append(int(arga))
    
                        elif argtype == discord.Role:
                            id = 0
                            if arga.startswith("<@&") and arga.endswith(">"):
                                id = int(arga[3:-1])
                            else:
                                id = int(arga)
                            args.append(await message.guild.fetch_role(id))
                        elif argtype == discord.Member:
                            id = 0
                            if arga.startswith("<@") and arga.endswith(">"):
                                id = int(arga[2:-1])
                            else:
                                id = int(arga)
                            args.append(await client.fetch_user(id))
                        elif argtype == bool:
                            args.append(bool(arga[0].upper()+arga[1:]))

                        indx += 1
                      except Exception as e:
                        ec = e.__class__
                        rep = message.reply
                        if ec == ValueError or ec == TypeError:
                            emb = discord.Embed(
                            title="Error",
                            description=f"Invalid argument type:\n\nThe '{argname}' argument was entered incorrectly. '{arga}' is not a {argtype.__name__}.")
                            emb.set_footer(text=f"Loud Bot")
                            emb.color = discord.Color.red()
                            await rep(embed=emb)
                            return
                        elif ec == IndexError:
                            emb = discord.Embed(
                                  title="Error",
                                  description=f"Invalid arguments:\n\nArgument not found for '{arga}'.",)
                            emb.set_footer(text=f"Loud Bot")
                            emb.color = discord.Color.red()
                            await rep(embed=emb)
                            return
                        else:
                            emb = discord.Embed(
                                  title="Error",
                                  description=f"Error parsing arguements:\n\n{e}")
                            emb.set_footer(text=f"Loud Bot")
                            emb.color = discord.Color.red()
                            await rep(embed=emb)
                            return
                
                args.insert(0, MI(message))

                args = tuple(args)
                await cmd(*args)
                if using in ["say", "dm"]:
                    await message.delete()
                            
                        
                        
                
        if message.reference and (ref_message := await message.channel.fetch_message(message.reference.message_id)):
            if ref_message.author == client.user:
                try:
                    messages = [message]
                    while messages[-1].reference:
                        ref_message = await message.channel.fetch_message(messages[-1].reference.message_id)
                        messages.append(ref_message)
                    messages.reverse()
        
                    alg = [{"role": "Assistant", "content": x.content} if x.author == client.user else {"role": x.author.name, "content": x.content} for x in messages]
        
                    await message.channel.typing()
                    response = await aigen(message, alg)
                    
                    await message.reply(response.replace("AI: ", "").replace("Assistant: ", "").replace("Ai: ", ""))
        
                except Exception as e:
                    await message.reply(f"{e.__class__.__name__}: {e}, line {e.__traceback__.tb_lineno}")
    try:
        if message.content.startswith(client.user.mention) or (
                message.channel.__class__ == discord.DMChannel and not message.reference):
            await message.channel.typing()
            response = await aigen(message, [{'role': 'user','content': message.content}])
            await message.reply(
                response.replace("AI: ",
                                      "").replace("Assistant: ",
                                                  "").replace("Ai: ", ""))
    except Exception as e:
        await message.reply(f"{e}")


try:
    token = ""
    
    client.run(token)
except discord.HTTPException as e:
    if e.status == 429:
        print(
            "The Discord servers denied the connection for making too many await requests"
        )
        print(
            "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyawait requests"
        )

sys.exit()