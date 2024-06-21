@tree.command(name = "servers", description = "shows the top 3 servers that loud bot is in")
async def name(interaction):
    s = db.getfile()["serverdata"]
    svrs = [emptyserver, emptyserver, emptyserver]
    for k, x in s.items():
        if len(x["users"].keys()) > len(svrs[0]["users"].keys()):
            svrs[0] = x
            continue
        if len(x["users"].keys()) > len(svrs[1]["users"].keys()):
            svrs[1] = x
            continue
        if len(x["users"].keys()) > len(svrs[2]["users"].keys()):
            svrs[2] = x
            continue
    mbed = discord.Embed(title="Top 3 loud bot servers:", color=discord.Color.blue())
    mbed.add_field(name=f"1. {svrs[0]['name']}", value=f"{len(svrs[0]['users'].keys())} members")
    mbed.add_field(name=f"2. {svrs[1]['name']}", value=f"{len(svrs[1]['users'].keys())} members")
    mbed.add_field(name=f"3. {svrs[2]['name']}", value=f"{len(svrs[2]['users'].keys())} members")

    mbed.set_thumbnail(url='https://media.discordapp.net/attachments/1128128913013485618/1235930140060680252/transitions-kinemaster.gif?ex=66362923&is=6634d7a3&hm=2a316cf0b322a62c5236fcc2b9f41f17e2bdbf9fca7f4f0e1d0e222bb964d8d2&')

    await interaction.response.send_message(embed=mbed)