from discord.ext import commands
from discord import app_commands, File
import json
import discord


class voicerecAPI(commands.Cog):
  def __init__(self, bot):
        self.bot = bot

  @app_commands.command(name="join", description="create free qr code !!")
  async def join(self, interaction):
     pass


async def setup(bot):    
  await bot.add_cog(voicerecAPI(bot))   