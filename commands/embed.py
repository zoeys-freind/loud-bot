@tree.command(name="embed", description="Creates an embed.")
async def create_embed(interaction,
                       title: str,
                       desc: str,
                       footer: str = "",
                       url: str = "",
                       image: str = "",
                       thumbnail: str = ""):
    embed = discord.Embed(timestamp=discord.utils.utcnow())
    embed.set_author(name=interaction.user.name,
                     icon_url=interaction.user.avatar)
    embed.title = title
    embed.description = desc
    if footer != "":
        embed.set_footer(text=footer)
    if url != "":
        embed.url = url

    if image != "":
        embed.set_image(url=image)
    if thumbnail != "":
        embed.set_thumbnail(url=thumbnail)
    await interaction.channel.send(embed=embed)
    await interaction.response.send_message(embed=discord.Embed(title="Embed created.", color=discord.Color.blue()), ephemeral=True)