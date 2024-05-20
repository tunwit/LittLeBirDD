import discord
from discord.ext import commands
import json
import wavelink as wavelink
from cogs.createsource import createsource
from discord import app_commands
import asyncio
import itertools
from ui.embed_gen import createembed
from ui.language_respound import get_respound
from ui.button import buttin
import math
import requests

class customplaylistAPI(commands.Cog):
  def __init__(self,bot):
    self.bot = bot
    self.replacer = '$^'
    self.replacement = '.'

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

  async def statistic(self,search):
      search = search.replace(self.replacement,self.replacer)
      if len(search) > 99:
        return
      try:
        get = requests.get(search)
        if get.status_code == 200:
          link =  True
        else:
          link =  False
      except:
        link =  False
      if link is not True:
        database = self.bot.mango['searchstatistic']
        data = database.find_one({})
        if search not in data['search']:
          database.update_one({},{'$set':{f'search.{search}':1}})
        else:
          database.update_one({},{'$inc':{f'search.{search}':1}})

  @app_commands.command(name="add_playlist",description="Add music to your private playlist")
  @app_commands.describe(search="Song name")
  async def add_playlist(self,interaction:discord.Interaction,search:str):    
      await interaction.response.defer()
      if await self.check_ban(interaction.user.id):
        respound = get_respound(interaction.locale,"baned")
        embed = createembed.baned(interaction,interaction.client,respound)
        d = await interaction.followup.send(embed=embed)
        await asyncio.sleep(5)
        await d.delete()
        return
      respound = get_respound(interaction.locale,"addplaylist")
      if not await self.check_vip(interaction.user.id):
        embed = createembed.addplaylistnovip(interaction,interaction.client,respound)
        d = await interaction.followup.send(embed=embed)
        await asyncio.sleep(5)
        await d.delete() 
        return
      source = await createsource.searchen(self,search,interaction.user)
      if source == None:
        embed = createembed.addplaylistnoresult(interaction,interaction.client,respound)
        d = await interaction.followup.send(embed=embed)
        await asyncio.sleep(5)
        await d.delete()
        return
      user = str(interaction.user.id)
      database = self.bot.mango['lplaylist']
      data = database.find_one({'user_id':user})
      if not data:
          database.insert_one({'user_id':user,
                               'playlist':{}})
      playlist = False
      if isinstance(source,wavelink.Playlist):
         playlist=True
         for track in source.tracks:
            name = track.title.replace(self.replacement, self.replacer)
            link = track.uri.replace(self.replacement, self.replacer)
            database.update_one({'user_id':user},{'$set':{f'playlist.{name}':link}})
      else:        
        name = source.title.replace(self.replacement, self.replacer)
        link = source.uri.replace(self.replacement, self.replacer)
        database.update_one({'user_id':user},{'$set':{f'playlist.{name}':link}})

      if playlist:
        embed = createembed.addplaylistsuccess(interaction,interaction.client,respound,source.tracks[0].title)
        embed.set_thumbnail(url = source.tracks[0].artwork)
      else:
        embed = createembed.addplaylistsuccess(interaction,interaction.client,respound,source.title)
        embed.set_thumbnail(url = source.artwork)
      await self.statistic(search)
      d = await interaction.followup.send(embed=embed)
      await asyncio.sleep(5)
      await d.delete()  
      return

  @add_playlist.autocomplete('search')
  async def fruits_autocomplete(self,interaction,current: str,):
        database = self.bot.mango["searchstatistic2"]
        source = database.find().sort("times", -1).limit(3)
        if len(current) > 0:
            source = database.find({"music": {"$regex": current}}).limit(25)
        return [app_commands.Choice(name=l["music"].replace(self.replacer, self.replacement),value=l["music"].replace(self.replacer, self.replacement))for l in source]
      
  @app_commands.command(name="ql_playlist",description="Send your private playlist")
  async def ql_playlist(self,interaction:discord.Interaction):
      await interaction.response.defer()
      if await self.check_ban(interaction.user.id):
        respound = get_respound(interaction.locale,"baned")
        embed = createembed.baned(interaction,interaction.client,respound)
        d = await interaction.followup.send(embed=embed)
        await asyncio.sleep(5)
        await d.delete()
        return
      database = self.bot.mango['lplaylist']
      data = database.find_one({'user_id':str(interaction.user.id)})
      respound = get_respound(interaction.locale,"ql_playlist")
      if await self.check_vip(interaction.user.id):
        if not data:
          embed = createembed.ql_playlistnolist(interaction,interaction.client,respound)
          d = await interaction.followup.send(embed=embed)
          await asyncio.sleep(5)
          await d.delete()  
          return
        pag = []
        number = len(data['playlist'])
        page = math.ceil(number/10)
        if page == 0:
          page = 1
        lists = []
        for s,i in zip(data['playlist'],range(len(data['playlist']))):
          op = f'{i+1}.{s.replace(self.replacer, self.replacement)}'
          lists.append(op)    
        for i in range(page):   
          upcoming = list(itertools.islice(lists, 0, 10))    
          if i != 0:
            fmt = '\n'.join(f'**` {_}`**' for _ in upcoming)
            embed = discord.Embed(color = 0xFFFFFF) 
          else:
            fmt = '\n'.join(f'**` {_}`**' for _ in upcoming)     
            embed = discord.Embed(color = 0xFFFFFF)    
          embed.add_field(name =respound.get("inlist"),value = f'{fmt}' ,inline = False)
          pag.append(embed)
          for i in range(10):
            try:
              del lists[0]
            except:pass
        view=buttin(pag,120,interaction)
        view.interaction=interaction
        await interaction.followup.send(embed = pag[0],view=view)
        return
      embed = createembed.ql_playlistnovip(interaction,interaction.client,respound)
      d = await interaction.followup.send(embed=embed)
      await asyncio.sleep(5)
      await d.delete()   

  @app_commands.command(name="remove_playlist",description="Remove music that given from your playlist")
  @app_commands.describe(number="Music sequence")
  async def remove_playlist(self,interaction:discord.Interaction,number:int):
      await interaction.response.defer()
      if await self.check_ban(interaction.user.id):
        respound = get_respound(interaction.locale,"baned")
        embed = createembed.baned(interaction,interaction.client,respound)
        d = await interaction.followup.send(embed=embed)
        await asyncio.sleep(5)
        await d.delete()
        return
      respound = get_respound(interaction.locale,"remove_playlist")
      if not await self.check_vip(interaction.user.id):
        embed = createembed.remove_playlistnovip(interaction,interaction.client,respound)
        d = await interaction.followup.send(embed=embed)
        await asyncio.sleep(5)
        await d.delete()  
        return
      database = self.bot.mango['lplaylist']
      data = database.find_one({'user_id':str(interaction.user.id)})
      if not data:
        embed = createembed.remove_playlistnolist(interaction,interaction.client,respound)
        d = await interaction.followup.send(embed=embed)
        await asyncio.sleep(5)
        await d.delete()     
        return
      embed = createembed.remove_playlistsuccess(interaction,interaction.client,respound,list(data['playlist'].keys())[number-1].replace(self.replacer, self.replacement))
      database.update_one({'user_id':str(interaction.user.id)}, {"$unset": {f"playlist.{list(data['playlist'].keys())[number-1]}": ""}})
      d = await interaction.followup.send(embed=embed)
      await asyncio.sleep(5)
      await d.delete() 
      return
  

  @app_commands.command(name="clear_playlist",description="Clear music from playlist")
  async def clear_playlist(self,interaction:discord.Interaction):
      await interaction.response.defer()
      if await self.check_ban(interaction.user.id):
        respound = get_respound(interaction.locale,"baned")
        embed = createembed.baned(interaction,interaction.client,respound)
        d = await interaction.followup.send(embed=embed)
        await asyncio.sleep(5)
        await d.delete()
        return
      respound = get_respound(interaction.locale,"clear_playlist")
      if not await self.check_vip(interaction.user.id):
        embed = createembed.clear_playlistfailed(interaction,interaction.client,respound)
        d = await interaction.followup.send(embed=embed)
        await asyncio.sleep(5)
        await d.delete() 
        return
      database = self.bot.mango['lplaylist']
      data = database.find_one({'user_id':str(interaction.user.id)})
      embed = createembed.clear_playlistsuccess(interaction,interaction.client,respound)
      database.delete_one({'user_id':str(interaction.user.id)})
      d = await interaction.followup.send(embed=embed)
      await asyncio.sleep(5)
      await d.delete()            
      return
         
    
async def setup(bot):
  await bot.add_cog(customplaylistAPI(bot))