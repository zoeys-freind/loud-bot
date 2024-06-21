@tree.command(name="goober-quote", description="Gets a random quote from goober's (zoeys_freind) messages.")
async def goober_quote(interaction):
    q = json.load(open("assets/gquotes.json", "r"))["quotes"]
    quote = random.choice(q)
    
    await interaction.response.send_message(embed=discord.Embed(title="A quote from goober.", description=f'"{quote}"', color=discord.Color.blue()))