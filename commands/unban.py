@tree.command(name="unban", description="Unbans a user from the server. admin+")
async def kick(interaction, user: discord.Member):
    try:
        usr = db.getserveruser(interaction.guild.id, user.id)
        iusr = db.getserveruser(interaction.guild.id, interaction.user.id)
        if iusr["admin"] or user.id == interaction.guild.owner_id:
            emb2 = discord.Embed(title="Unban", description=f"You have been unbanned from {interaction.guild.name}.", color=discord.Color.green())
            user.send(embed=emb2)
            user.unban()
            emb = discord.Embed(title="Unan", description=f"{user.mention} has been unbanned from the server by {interaction.user.mention}.", color=discord.Color.yellow())
            await interaction.response.send_message(embed=emb)
        else:
            await interaction.response.send_message(embed=discord.Embed(title="Missing permissions", description="You do not have permission to use this command.", color=discord.Color.red()), ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(embed=error_embed(e))