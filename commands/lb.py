@tree.command(name="lb", description="Shows the top 10 users in the server.")
async def leaderboard(interaction):
    dbc = db.getserver(interaction.guild.id)["users"]
    leaderboard = sorted(dbc.items(),
                         key=lambda x: x[1]['level'],
                         reverse=True)[:10]
    embed = discord.Embed(title="Top 10 Users:", color=discord.Color.blue())
    for i, (user_id, user_data) in enumerate(leaderboard):
        try:
            member = interaction.channel.guild.get_member(int(user_id))
            embed.add_field(name=f"{i+1}. {member.name}", value=f"Level: {user_data['level']}")
        except Exception as e:
            print(f"Error {e}")
    await interaction.response.send_message(embed=embed)