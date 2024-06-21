class ConfigForm(discord.ui.Modal):

    def __init__(self, svrid, oint):
        self.svr = db.getserver(svrid)
        self.PREFIX = discord.ui.TextInput(
        label='Prefix',
        style=discord.TextStyle.short,
        required=False,
        placeholder=self.svr["config"]["prefix"]
        )
        self.MODROLE = discord.ui.Select(custom_id="Modrole", placeholder=str(oint.guild.get_role(svrid)), min_values=1, max_values=1, options=[a.name for a in oint.guild.roles], disabled=False)
        
        
        super().__init__(title='Loud Bot Server Config')
        self.oint = oint
        self.configure = {
            "prefix": self.svr["config"]["prefix"],
            "modrole": self.svr["config"]["modrole"],
            "adminrole": self.svr["config"]["adminrole"],
            "color": self.svr["config"]["color"]
        }
    

    

    async def on_submit(self, interaction: discord.Interaction):
        if self.PREFIX != "":
            self.configure["prefix"] = str(self.PREFIX)
        print(self.configure)
        await interaction.response.send_message(embed=discord.Embed(title="Config saved!", description="All configurations have been saved. Empty inputs have been replaced with the existing configurations.", color=discord.Color.green()), ephemeral=True)
        
class ConfigSelection(discord.ui.View):
    def __init__(self, svrid, oint):
        super().__init__(timeout = None)
        self.svrid = svrid
        self.oint = oint
    @discord.ui.button(label = "Open form", custom_id = "open", style = discord.ButtonStyle.blurple)
    async def bttn(self, interaction: discord.Interaction, button:discord.Button):
        await interaction.response.send_modal(ConfigForm(self.svrid, self.oint))
        
@tree.command(name="config-server", description="Configures the server. admin+")
async def config_server(interaction):
    usr = db.getserveruser(str(interaction.guild.id), str(interaction.user.id))
    if usr["admin"] or interaction.user.id == interaction.guild.owner_id:
        
        await interaction.response.send_message(embed=discord.Embed(title="Configuring...", color=discord.Color.blue()), ephemeral=True, view=ConfigSelection(str(interaction.guild.id), interaction))
        
    else:
        await interaction.response.send_message(embed=discord.Embed(title="Missing permissions", description="You do not have permission to use this command.", color=discord.Color.red()), ephemeral=True)