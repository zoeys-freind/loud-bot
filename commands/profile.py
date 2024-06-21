@tree.command(name="profile", description="sends your profile card.")
async def profile(interaction,
                  user: discord.Member = None,
                  config: bool = False):
    if user is None:
        user = interaction.user
    if user.bot == False:
        if not config:
            template = Image.new("RGBA", (780, 350), (20, 20, 60))
            season = "./assets/pfdd.png"
            gtemplate = Image.open(season)
            template.paste(gtemplate, (0, 0))
            avatar_url = user.display_avatar.url
            print(avatar_url)
            avatar_data = (await requests.get(avatar_url)).content
            print('gt')

            avatar_image = Image.open(BytesIO(avatar_data))
            avatar_image = avatar_image.resize((300, 300))
            # add background shadow
            shadow = Image.new("RGBA", avatar_image.size, (20, 20, 60, 80))

            template.paste(shadow, (5, 8))
            template.paste(avatar_image, (15, 18))
            # add big text with username
            font = ImageFont.truetype("./assets/DejaVuSansMono-Bold.ttf", size=40)
            draw = ImageDraw.Draw(template)
            draw.text((335, 18), user.name, (255, 255, 255), font=font)
            # add small text with level
            usr = db.getserver(interaction.guild.id)["users"][str(user.id)]
            if user.top_role.name.endswith("s"):
                tprl = user.top_role.name[:-1]
            else:
                tprl = user.top_role.name
            font = ImageFont.truetype("./assets/DejaVuSansMono-Bold.ttf", size=30)
            draw.text((335, 58),
                      tprl,
                      hex_to_rgb(user.top_role.color),
                      font=font)
            font = ImageFont.truetype("./assets/DejaVuSansMono.ttf", size=20)

            draw.text(
                (335, 90),
                f"{create_progress_bar(usr['xp']-(usr['level']-1) * (usr['level']-1) + 1, ((usr['level'] * usr['level']) + 1)-(usr['level']-1) * (usr['level']-1) + 1, 30)}\nLevel: {usr['level']}\nXP: {usr['xp']}\n# of warns: {len(usr['warns'])}\nAdmin: {user.top_role.permissions.administrator}\n",
                (255, 255, 255),
                font=font)

            barr = BytesIO()
            template.save(barr, format="PNG")
            barr.name="profile.png"
            barr.seek(0)

            await interaction.response.send_message(file=discord.File(barr))
    else:
        await interaction.response.send_message(embed=discord.Embed(title="You can't use this command on bots!", color=discord.Color.red()), ephemeral=True)