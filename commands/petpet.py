@tree.command(name="petpet", description="PAT THEM")
async def petpet(ctx, file: discord.Attachment):
    r = BytesIO((await requests.get(file.proxy_url)).content)
    dest = BytesIO()
    petpetgif.make(r, dest)
    dest.seek(0)
    await ctx.response.send_message(file=discord.File(dest, filename=f"petpet.gif"))