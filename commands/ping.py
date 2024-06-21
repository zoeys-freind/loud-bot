@tree.command(name="ping", description="Checks the bot's latency and ping.")
async def ping(interaction):
    embed = discord.Embed(title="Pong!", color=discord.Color.blue())
    embed.add_field(name="Latency", value=f"{client.latency}")
    embed.add_field(name="Ping", value=f"{round(client.latency * 1000)}ms")
    await interaction.response.send_message(embed=embed)
    print(interaction.guild.icon)