@tree.command(
    name="edit-permissions",
    description="Allows you to edit a user's mod/admin permission. Admin+")
async def admin_add(interaction,
                    user: discord.User,
                    admin: bool = None,
                    mod: bool = None):
    usrjsn = db.getserveruser(interaction.guild.id, interaction.user.id)

    if usrjsn["admin"] or interaction.user.id == interaction.guild.owner.id:
        if check_high(
                interaction.user,
                user) or interaction.user.id == interaction.guild.owner.id:
            usrjsn["admin"] = admin
            usrjsn["mod"] = mod
            asb = db.getserveruser(interaction.guild.id, interaction.user.id)
            asb.update(usrjsn)
            db.saveserveruser(interaction.guild.id, interaction.user.id, asb)
            await interaction.response.send_message(
                f"Successfully set {user.name}'s admin/mod permission to {admin} and {mod}."
            )

        else:
            await interaction.response.send_message(
                embed=discord.Embed(title="Missing permissions", description="You cannot edit someone's permissions if they are higher than you.", color=discord.Color.red()),
            )

    else:
        await interaction.response.send_message(
            embed=discord.Embed(title="Missing permissions", description="You do not have permission to use this command.", color=discord.Color.red()),
        )