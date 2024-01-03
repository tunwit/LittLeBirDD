from typing import Optional
import discord
import random
import json
import akaneko
from discord.ext import commands
import giphy_client 
from giphy_client.rest import ApiException
from discord import app_commands
from discord.app_commands import Choice
import asyncio
from ui.embed_gen import createembed
from ui.language_respound import get_respound
  
class imageAPI(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  async def check_ban(self,v):
      if self.bot.mango['ban'].find_one({'user_id':str(v)}):
        return True
      else:
        return False

  @app_commands.command(name="gif",description="Send gif")
  @app_commands.describe(search="search for gif")
  async def gif(self,interaction:discord.Interaction,search:Optional[str]="defualt"):
    await interaction.response.defer()
    if await self.check_ban(interaction.user.id):
        respound = get_respound(interaction.locale,"baned")
        embed = createembed.baned(interaction,interaction.client,respound)
        d = await interaction.followup.send(embed=embed)
        await asyncio.sleep(5)
        await d.delete()
        return
    if await self.check_ban(interaction.user.id):
        respound = get_respound(interaction.locale,"baned")
        embed = createembed.baned(interaction,interaction.client,respound)
        d = await interaction.followup.send(embed=embed)
        await asyncio.sleep(5)
        await d.delete()
        return
    try:
      api_key = 'jYu1Ih2J3gzF5hgIjo1u1p7HnJJ6NByn'
      api_instance = giphy_client.DefaultApi()
      limit = 25
      tag = 'laugh'
      rating = 'r'
      lang = 'th'

      if search == 'defualt':
        api_response = api_instance.gifs_random_get(api_key,tag=tag,rating=rating)
        url = api_response.data.url
        await interaction.followup.send(url)
      else:
        api_response = api_instance.gifs_search_get(api_key,search,limit=limit,rating=rating,lang=lang)
        lst = list(api_response.data)
        url = random.choice(lst)
        await interaction.followup.send(url.embed_url)
          
    except ApiException as e:
        respound = get_respound(interaction.locale,"gif")
        embed = createembed.gif(interaction,self.bot,respound)       
        d = await interaction.followup.send(embed=embed) 
        await asyncio.sleep(5)
        await d.delete()
        
  @app_commands.command(name="anime",description="Send anaime pic")
  @app_commands.describe(search="search for NFSW pic")
  @app_commands.choices(search=[
    Choice(name = "BDSM",value="bdsm"),
    Choice(name = "Doujin",value="doujin"),
    Choice(name = "Cum",value="cum"),
    Choice(name = "Hentai",value="hentai"),
    Choice(name = "Yuri",value="yuri"),
    Choice(name = "Pussy",value="pussy"),
    Choice(name = "Maid",value="maid"),
    Choice(name = "Glasses",value="glasses"),
    Choice(name = "Gifs",value="gifs"),
    Choice(name = "Blowjob",value="blowjob")])  
  async def anime(self,interaction:discord.Interaction,search:Optional[str]="normal"):
      await interaction.response.defer()
      if await self.check_ban(interaction.user.id):
        respound = get_respound(interaction.locale,"baned")
        embed = createembed.baned(interaction,interaction.client,respound)
        d = await interaction.followup.send(embed=embed)
        await asyncio.sleep(5)
        await d.delete()
        return
      respound = get_respound(interaction.locale,"anime")
      if search == 'normal':
            rType = [akaneko.sfw.neko(),akaneko.sfw.foxgirl()]
            r = random.choice(rType)
            await interaction.followup.send(r)
            return
      if interaction.channel.is_nsfw():
        try:
          if search == 'bdsm':
                await interaction.followup.send(akaneko.nsfw.bdsm())
          elif search == 'doujin':
                await interaction.followup.send(akaneko.nsfw.doujin())
          elif search == 'cum':
                await interaction.followup.send(akaneko.nsfw.cum())
          elif search == 'hentai':
                await interaction.followup.send(akaneko.nsfw.hentai())
          elif search == 'yuri':
                await interaction.followup.send(akaneko.nsfw.yuri())   
          elif search == 'pussy':
                await interaction.followup.send(akaneko.nsfw.pussy())
          elif search == 'maid':
                await interaction.followup.send(akaneko.nsfw.maid())   
          elif search == 'glasses':
                await interaction.followup.send(akaneko.nsfw.glasses())
          elif search == 'gifs':
                await interaction.followup.send(akaneko.nsfw.gifs())
          elif search == 'blowjob':
                await interaction.followup.send(akaneko.nsfw.blowjob())
          else:
            await interaction.followup.send("Not found")
        except:
              embed = createembed.anime(interaction,self.bot,respound)       
              d = await interaction.followup.send(embed=embed)   
              await asyncio.sleep(5)
              await d.delete()
      else:
          embed = createembed.anime(interaction,self.bot,respound,nsfw=True)       
          d = await interaction.followup.send(embed=embed)
          await asyncio.sleep(5)
          await d.delete()

async def setup(bot):
  await bot.add_cog(imageAPI(bot)) 