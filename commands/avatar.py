@tree.command(name = "avatar", description = "Sends a user's avatar.")
async def name(interaction, user:discord.Member):
    try:
        embed = discord.Embed(title=f"{user.name}'s avatar", color=discord.Color.blue())
        embed.set_image(url=user.avatar.url)
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        await interaction.response.send_message(embed=error_embed(e))