@tree.command(name="quote", description="Quotes a message (by ID)")
async def quote(interaction, message_id: str):
    message = await interaction.channel.fetch_message(message_id)
    gradient = Image.open("./assets/quote-bg.png")
    gradient = gradient.convert("RGBA")
    req = await requests.get(str(message.author.avatar))

    image = Image.open(BytesIO(req.content))
    image = image.convert("RGBA")
    bg = Image.new("RGBA", (1080, 750), "white")
    image = image.resize((1080, 1080))
    mask = gradient.split()[3]

    bg.paste(image, (0, -270))

    bg.paste(gradient, (0, 0), mask)
    font = ImageFont.truetype("./assets/DejaVuSansMono-Bold.ttf", size=40)
    draw = ImageDraw.Draw(bg)

    # wrap text with newlines.
    wrappable = message.content
    final = ""
    indx = 0
    for x in wrappable.split(" "):
        final += x + " "
        if indx >= 4 or len(x) > 10:
            final += "\n"
            indx = 0
        indx += 1

    draw.text((50, 50), final, font=font, fill=(255, 255, 255, 255))
    draw.text((350, 650),
              f"- {message.author.name}, {datetime.datetime.now().year}",
              font=font,
              fill=(255, 255, 255, 255))

    barr = BytesIO()
    bg.save(barr, format="PNG")
    barr.name="quote.png"
    barr.seek(0)

    await interaction.response.send_message(file=discord.File(barr))