@tree.command(name="shutdown", description="Turns off the bot. Dev+")
async def shutdown(interaction, reason: str = "no reason given"):
    if str(interaction.user.id) == str(goobuhid):
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Shutting down...",
                description=f"Reason: \"{reason}\"",
                color=discord.Color.yellow())
        )
        exit()
    else:
        await interaction.response.send_message(
            embed=discord.Embed(title="Missing permissions", description="You do not have permission to use this command.", color=discord.Color.red()),
        )