@tree.command(name="help", description="Sends the help menu.")
async def help(interaction):
    embed = discord.Embed(title="Help menu", description="Loud bot v2", color=discord.Color.blue())
    for x in tree.get_commands():
        embed.add_field(name="/"+x.name, value=x.description)
    await interaction.response.send_message(embed=embed, ephemeral=True)