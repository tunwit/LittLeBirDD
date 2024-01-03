from win32com import client
import discord
from discord.ext import commands
import random
from discord import app_commands
import asyncio
import os
import comtypes.client


class convertAPI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.path = "cf"

    async def doc_to_pdf(self, file, name: str):
        await file.save(f"./cf/{name}.docx")
        word = comtypes.client.CreateObject("Word.Application")
        doc = word.Documents.Open(f"{self.path}{name}.docx")
        doc.SaveAs(f"{self.path}{name}.pdf", FileFormat=17)
        doc.Close()
        word.Quit()

    async def doc_to_pdf(self, file, name: str):
        await file.save(f"./cf/{name}.docx")
        word = comtypes.client.CreateObject("Word.Application")
        doc = word.Documents.Open(f"{self.path}{name}.docx")
        doc.SaveAs(f"{self.path}{name}.pdf", FileFormat=17)
        doc.Close()
        word.Quit()

    async def xlsx_to_pdf(self, file, name: str):
        await file.save(f"./cf/{name}.xlsx")
        excel = client.Dispatch("Excel.Application")
        excel.Interactive = False
        excel.Visible = False
        sheets = excel.Workbooks.Open(f"{self.path}{name}.xlsx")
        sheets.ExportAsFixedFormat(0, f"{self.path}{name}.pdf")
        sheets.Close()
        excel.Quit()

    async def clearfileinf(self, name: str, extention: str):
        os.remove(f"{self.path}{name}{extention}")
        os.remove(f"{self.path}{name}.pdf")

    @app_commands.command(name="pdf", description="To convert file to pdf")
    async def pdf(self, interaction: discord.Interaction, file: discord.Attachment):
        await interaction.response.defer()
        name = str(random.randint(1, 999999))
        if file.filename.endswith(".xlsx"):
            await self.xlsx_to_pdf(file, name)
            extention = ".xlsx"
        elif file.filename.endswith(".docx"):
            await self.doc_to_pdf(file, name)
            extention = ".docx"
        else:
            d = await interaction.followup.send("Unsupported file!!")
            await asyncio.sleep(5)
            await d.delete()
            return
        await interaction.followup.send(
            file=discord.File(
                fp=f"{self.path}{name}.pdf", filename=f"Please rename this file.pdf"
            )
        )
        await self.clearfileinf(name, extention)


async def setup(bot):
    await bot.add_cog(convertAPI(bot))
