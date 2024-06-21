@app_commands.choices(activity_type=[
    app_commands.Choice(name="Playing",value="playing"),
    app_commands.Choice(name="Listening to",value="listening"),
    app_commands.Choice(name="Watching",value="watching"),
    app_commands.Choice(name="Streaming",value="streaming")
])
@tree.command(name="change-activity", description="Changes the bot's activity.")
async def change_activity(interaction, activity_type:app_commands.Choice[str], text:str):
    datsv = json.load(open("./datsv.json", "r"))
    datsv["status"][0] = activity_type.value
    datsv["status"][1] = text

    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=getattr(discord.ActivityType, datsv["status"][0]), name=datsv["status"][1]))

    json.dump(datsv, open("./datsv.json", "w"), indent=4)
    await interaction.response.send_message(embed=discord.Embed(title="Changed activity!", description=f"Changed activity to {activity_type.name} {text}.", color=discord.Color.blue()), ephemeral=True)