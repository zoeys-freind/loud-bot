class RetryView(View):
    def __init__(self, header1, oint, cl):
        super().__init__()
        self.header = header1
        self.oint = oint
        self.catlist = cl

    @discord.ui.button(label="Retry", style=discord.ButtonStyle.blurple, custom_id="retry")
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.oint.user.id == interaction.user.id:
            nr = await requests.get("https://api.thecatapi.com/v1/images/search")
            chance = (random.randint(1, 100)==1 or self.header=="SOG")
            self.catlist.append(nr.json()[0]["url"] if not chance else "https://media.tenor.com/eXRp4UsPJlYAAAAC/soggy-cat-shark.gif")
        
            
            n_embed = discord.Embed(title=self.header, color=discord.Color.blue())
            n_embed.set_image(url=self.catlist[-1])
            n_embed.set_footer(text="Powered by thecatapi.com")
            await interaction.response.edit_message(embed=n_embed)
        else:
            await interaction.response.send_message(content="Nuh uh", ephemeral=True)
    
    @discord.ui.button(label="Back", style=discord.ButtonStyle.red, custom_id="back")
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.oint.user.id == interaction.user.id and len(self.catlist) > 1:
            self.catlist.pop()
            n_embed = discord.Embed(title=self.header, color=discord.Color.blue())
            n_embed.set_image(url=self.catlist[-1])
            n_embed.set_footer(text="Powered by thecatapi.com")
            await interaction.response.edit_message(embed=n_embed)
        else:
            await interaction.response.send_message(content="Nuh uh", ephemeral=True)
            
 
@tree.command(name="cat", description="Gets a random cat image from thecatapi.")
async def cat(interaction, header:str="A cat for you!"):
    r = await requests.get("https://api.thecatapi.com/v1/images/search")
    chance = (random.randint(1, 100)==1 or header=="SOG")
    CATLIST = []
    CATLIST.append(r.json()[0]["url"] if not chance else "https://media.tenor.com/eXRp4UsPJlYAAAAC/soggy-cat-shark.gif")

    embed = discord.Embed(title=header, color=discord.Color.blue())
    embed.set_image(url=CATLIST[-1])
    embed.set_footer(text="Powered by thecatapi.com")

    await interaction.response.send_message(embed=embed, view=RetryView(header, interaction, CATLIST))