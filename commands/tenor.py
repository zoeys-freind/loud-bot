@tree.command(name="tenor", description="Searches tenor for the first gif that matches the query.")
async def tenor(interaction, query:str, index:int=1):
    try:
        gif = await stenor(query, index)
        embed = discord.Embed(title=f"Result for '{query}'", color=discord.Color.blue())
        embed.set_image(url=gif)
        print(gif)
        embed.set_footer(text="Powered by tenor.com")
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        await interaction.response.send_message(embed=error_embed(e))