import discord
from discord.ext import commands
from discord_together import DiscordTogether
import json
from discord import app_commands
from discord.app_commands import Choice
import asyncio
from ui.language_respound import get_respound
from ui.help_embed import embed
from ui.button import buttin
from ui.embed_gen import createembed
from config import TOKEN

class chess(commands.Cog):
  def __init__(self, bot ):
    self.bot = bot

  async def check_ban(self,v):
      if self.bot.mango['ban'].find_one({'user_id':str(v)}):
        return True
      else:
        return False

  @app_commands.command(name="activities",description="play game with your friends")
  @app_commands.describe(activity="Choose activities")
  @app_commands.choices(activity=[
  Choice(name = "Chess",value="chess"),
  Choice(name = "Ocho",value="ocho"),
  Choice(name = "Poker",value="poker"),
  Choice(name = "Wordsnack",value="wordsnack"),
  Choice(name = "Youtube",value="youtube")])
  async def activity(self,interaction:discord.Interaction,activity:str):
      await interaction.response.defer()
      if await self.check_ban(interaction.user.id):
        respound = get_respound(interaction.locale,"baned")
        embed = createembed.baned(interaction,interaction.client,respound)
        d = await interaction.followup.send(embed=embed)
        await asyncio.sleep(5)
        await d.delete()
        return
      self.bot.togetherControl = await DiscordTogether(TOKEN)
      respound = get_respound(interaction.locale,"activity")
      if activity == "chess":
        link = await self.bot.togetherControl.create_link(interaction.user.voice.channel.id,'chess')
        d = await interaction.followup.send(respound.get("chess").format(link=link))
        await asyncio.sleep(25)
        await d.delete()
      elif activity == "ocho":
        link = await self.bot.togetherControl.create_link(interaction.user.voice.channel.id,'832025144389533716')
        d = await interaction.followup.send(respound.get("ocho").format(link=link))
        await asyncio.sleep(25)
        await d.delete()
      elif activity == "poker":
        link = await self.bot.togetherControl.create_link(interaction.user.voice.channel.id,'poker')
        d = await interaction.followup.send(respound.get("poker").format(link=link))
        await asyncio.sleep(25)
        await d.delete()
      elif activity == "wordsnack":
        link = await self.bot.togetherControl.create_link(interaction.user.voice.channel.id,'word-snack')
        d = await interaction.followup.send(respound.get("word").format(link=link))
        await asyncio.sleep(25)
        await d.delete()
      elif activity == "youtube":
        link = await self.bot.togetherControl.create_link(interaction.user.voice.channel.id,'youtube')
        d = await interaction.followup.send(respound.get("watch").format(link=link))
        await asyncio.sleep(25)
        await d.delete()  
    
async def setup(bot):    
  await bot.add_cog(chess(bot))        
