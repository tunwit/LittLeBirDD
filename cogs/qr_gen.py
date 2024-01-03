import discord
from discord.ext import commands
import json
from discord import app_commands, File
import asyncio
import qrcode
import io
from ui.embed_gen import createembed
from ui.language_respound import get_respound


class qrAPI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="qrcode", description="create free qr code !!")
    async def qr(self, interaction: discord.Interaction, text: str):
        await interaction.response.defer()
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=1,
        )
        qr.add_data(text)
        img = qr.make_image(fill_color="black", back_color="white")
        with io.BytesIO() as image_binary:
            img.save(image_binary, format="PNG")
            image_binary.seek(0)
            await interaction.followup.send(
                content=f"This is QR CODE for ` {text} ` ",
                file=File(fp=image_binary, filename="image.png"),
            )


async def setup(bot):
    await bot.add_cog(qrAPI(bot))
