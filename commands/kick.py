@tree.command(name="kick", description="Kicks a user from the server. mod+")
async def kick(interaction, user: discord.Member, reason: str = "No reason given.", fake: bool = False):
    try:
        usr = db.getserveruser(interaction.guild.id, user.id)
        iusr = db.getserveruser(interaction.guild.id, interaction.user.id)
        if iusr["mod"] or iusr["admin"] or user.id == interaction.guild.owner_id:
            if check_high(interaction.user, user) or user.id == interaction.guild.owner_id:
                if fake:
                    emb = discord.Embed(title="Kick", description=f"{user.mention} has been kicked from the server by {interaction.user.mention}.", color=discord.Color.yellow())
                    emb.add_field(name="Reason", value=reason)
                    await interaction.response.send_message(embed=emb)
                else:
                    emb2 = discord.Embed(title="Kick", description=f"You have been kicked from {interaction.guild.name}.", color=discord.Color.red())
                    emb2.add_field(name="Reason", value=reason)
                    user.send(embed=emb2)
                    user.kick(reason=reason)
                    s = db.getserver(interaction.guild.id)
                    del s["users"][str(user.id)]
                    db.saveserver(interaction.guild.id, s)
                    emb = discord.Embed(title="Kick", description=f"{user.mention} has been kicked from the server by {interaction.user.mention}.", color=discord.Color.yellow())
                    emb.add_field(name="Reason", value=reason)
                    await interaction.response.send_message(embed=emb)
            else:
                await interaction.response.send_message(embed=discord.Embed(title="Missing permissions", description="You can't kick someone higher than you.", color=discord.Color.red()), ephemeral=True)
        else:
            await interaction.response.send_message(embed=discord.Embed(title="Missing permissions", description="You do not have permission to use this command.", color=discord.Color.red()), ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(embed=error_embed(e))