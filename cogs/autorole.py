import discord
from discord.ext import commands
import json
from discord import app_commands
from ui.embed_gen import createembed
from ui.language_respound import get_respound

class autoroleAPI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="auto_role",description="give role to any user who join server")
    async def auto_role(self,interaction:discord.Interaction,role:discord.Role):
       print(role)



async def setup(bot):    
  await bot.add_cog(autoroleAPI(bot))   