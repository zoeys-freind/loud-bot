@tree.command(name="dm", description="DMs a user.")
async def dm(interaction, user: discord.Member, message: str):
    try:
        emb = discord.Embed(title=f"Message from {interaction.guild.name}!", description=f'"{message}"', color=discord.Color.blue())
        emb.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
        await user.send(embed=emb)
        await interaction.response.send_message(embed=discord.Embed(title=f"Sent to {user.name}!", color=discord.Color.green()), ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(embed=error_embed(e), ephemeral=True)