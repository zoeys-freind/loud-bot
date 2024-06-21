@tree.command(name="purge", description="Deletes a specified number of messages. admin+")
async def purge(interaction, amount: int):
    usr = db.getserveruser(interaction.guild.id, interaction.user.id)
    if usr["admin"] or interaction.user.id == interaction.guild.owner_id:
        await interaction.response.send_message("Deleting..."
, ephemeral=True)
        await interaction.channel.purge(limit=amount)
        await interaction.channel.send(embed=discord.Embed(title="Purge", description="Purged " + str(amount) + " messages.", color=discord.Color.blue()))