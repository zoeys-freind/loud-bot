@tree.command(name="say", description="Broadcasts a message.")
async def say(interaction, message:str=None, reply_id:str="", attachment:discord.Attachment=None):
    try:
        repmssg = None
        embed = None
        if reply_id != "":
            repmssg = await interaction.channel.fetch_message(reply_id)
            await repmssg.reply(message)
            embed = discord.Embed(title="Sent!", description=f"Replied to {repmssg.author.name}.", color=discord.Color.blue())
        else:
            if attachment == None:
                await interaction.channel.send(message)
            else:
                FILE = BytesIO((await requests.get(attachment.proxy_url)).content) if attachment else None
                if FILE:
                    FILE.seek(0)
                await interaction.channel.send(message, file=discord.File(FILE, filename=attachment.filename) if attachment else None)
            chnl = "DM"
            if interaction.channel.__class__ != discord.DMChannel:
                chnl = "#"+interaction.channel.name
            embed = discord.Embed(title="Sent!", description=f"Sent to {chnl}.", color=discord.Color.blue())
        await interaction.response.send_message(embed=embed, ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(embed=error_embed(e), ephemeral=True)