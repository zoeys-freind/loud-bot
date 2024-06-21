class RefreshView(View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Refresh", style=discord.ButtonStyle.blurple, custom_id="refresh")
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        now = datetime.now()
        embed = discord.Embed(title="Loud bot time", description="the local time for loud bot.", color=discord.Color.blue())
        embed.add_field(name="12-hour", value=now.strftime("%I:%M:%S %p"))
        embed.add_field(name="24-hour", value=now.strftime("%H:%M:%S"))
        embed.add_field(name="Date", value=now.strftime("%Y-%m-%d (y-m-d)"))
        await interaction.response.edit_message(embed=embed)


@tree.command(name="time", description="Gets loud bot's local time.")
async def _time(interaction):
    now = datetime.now()
    embed = discord.Embed(title="Loud bot time", description="the local time for loud bot.", color=discord.Color.blue())
    embed.add_field(name="12-hour", value=now.strftime("%I:%M:%S %p"))
    embed.add_field(name="24-hour", value=now.strftime("%H:%M:%S"))
    embed.add_field(name="Date", value=now.strftime("%Y-%m-%d (y-m-d)"))
    await interaction.response.send_message(embed=embed, view=RefreshView())