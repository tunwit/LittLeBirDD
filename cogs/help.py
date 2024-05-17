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
import asyncio

class helpAPI(commands.Cog):
  def __init__(self,bot):
    self.bot = bot

  async def check_ban(self,v):
      if self.bot.mango['ban'].find_one({'user_id':str(v)}):
        return True
      else:
        return False
      
  async def check_vip(self,v):
      if self.bot.mango['vip'].find_one({'user_id':str(v)}):
        return True
      else:
        return False
        
  @app_commands.command(name="help",description="Send all commands")
  async def help(self,interaction:discord.Interaction):
    await interaction.response.defer()
    if await self.check_ban(interaction.user.id):
        respound = get_respound(interaction.locale,"baned")
        embed = createembed.baned(interaction,interaction.client,respound)
        d = await interaction.followup.send(embed=embed)
        await asyncio.sleep(5)
        await d.delete()
        return
    respound = get_respound(interaction.locale,"help")
    pages = e.embed(self.bot,respound,interaction)
    but_ton=buttin(pages,120,interaction)
    but_ton.interaction = interaction
    await interaction.followup.send(embed = pages[0],view=but_ton)

async def setup(bot):
  await bot.add_cog(helpAPI(bot))
