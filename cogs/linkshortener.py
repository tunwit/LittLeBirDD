from typing import List
from colorama import Style
import discord
from discord.ext import commands
import json
from discord import app_commands
from ui.embed_gen import createembed
from ui.language_respound import get_respound
from ui.help_embed import embed as e
from ui.button import buttin
import requests
import asyncio

class linkshortenerAPI(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    async def check_ban(self,v):
      if self.bot.mango['ban'].find_one({'user_id':str(v)}):
        return True
      else:
        return False
      
    @app_commands.command(name="linkshortener",description="shorten your link")
    @app_commands.describe(url="link or url")
    async def linkshortener(self,interaction:discord.Interaction,url:str):
        await interaction.response.defer()
        if await self.check_ban(interaction.user.id):
          respound = get_respound(interaction.locale,"baned")
          embed = createembed.embed_fail(interaction,respound)
          d = await interaction.followup.send(embed=embed)
          await asyncio.sleep(5)
          await d.delete()
          return
        result = requests.post('https://littleshort.vercel.app/api/link',json={"origin":url})
        if result.status_code == 201:
            await interaction.followup.send(f'https://littleshort.vercel.app/{result.json()["data"]["uniqueID"]}')
        else:
            await interaction.followup.send(f'There is an error occured status code {result.status_code}')

async def setup(bot):
  await bot.add_cog(linkshortenerAPI(bot))