import discord
from discord.ext import commands,tasks
import json
from discord import app_commands
import asyncio
from ui.embed_gen import createembed
from ui.language_respound import get_respound
from youtubesearchpython import *
from discord.ui import Button,View
import scrapetube
from discord.ui import View, Button , button
import requests
from bs4 import BeautifulSoup
import math
import itertools
from ui.button import buttin
import re

class check(View):
    def __init__(self,interaction,channel,bot):
        super().__init__()
        self.interaction = interaction
        self.origin = None
        self.channel = channel
        self.bot = bot

    async def get_recent_video(self,url):
        try:
          html = requests.get(url + "/videos").text
          video = re.search('(?<="videoId":").*?(?=")', html).group()
        except:
          video = None

        try:
          html = requests.get(url + "/streams").text
          stream = re.search('(?<="videoId":").*?(?=")', html).group()
        except:
          stream = None

        return {"video":video,"stream":stream}

    @button(label="Yes",style=discord.ButtonStyle.green)
    async def yes(self,interaction:discord.Interaction,button):
        await interaction.response.defer()
        with open("database/notification.json", "r",encoding="utf8") as f:
              database = json.load(f)
        data = Channel.get(self.channel)
        recent = await self.get_recent_video(data["url"])
        if database.get(str(interaction.guild.id),None) == None:
          database[str(interaction.guild.id)] = {
            f"{data['title']}":{
              "recent_video":recent["video"],
              "recent_stream":recent["stream"],
              # "yt_channel_id":self.channel,
              "yt_channel":data["id"],
              "dc_channel":str(interaction.channel.id)
            }
          }
          await interaction.followup.send("Success")
        else:
          if database[str(interaction.guild.id)].get(str(data['title']),None) == None:
            new = {
              f"{data['title']}":{
                "recent_video":recent["video"],
                "recent_stream":recent["stream"],
                "yt_channel":data["id"],
                "dc_channel":str(interaction.channel.id)
              }
            }
            database[str(interaction.guild.id)].update(new)
            await interaction.followup.send("Success")
          else:
            await interaction.followup.send("That channel is already exist")

        with open("database/notification.json", "w" ,encoding="utf8") as f:
              json.dump(database,f,ensure_ascii=False,indent=4)
        await self.origin.delete()
        try:
          await interaction.followup.send(content="")
        except:pass

    @button(label="No",style=discord.ButtonStyle.red)
    async def no(self,interaction:discord.Interaction,button):
      await interaction.response.defer()
      await self.origin.delete()
      await interaction.followup.send("Canceled")
      try:
        await interaction.followup.send(content="")
      except:pass

class notifyAPI(commands.Cog):
    def __init__(self,bot):
        self.bot:commands.Bot = bot

    async def get_channel(self,channel:str):
      result = None
      b = False
      for i in self.bot.guilds:
        if b:
          break
        channelid = int(channel)
        for c in i.channels:
          if c.id == channelid:
              result = c , i
              b = True
              break
      return result
    
    async def get_recent_video(self,url):
        url = "https://www.youtube.com/channel/" + url
        try:
          html = requests.get(url + "/videos").text
          video = re.search('(?<="videoId":").*?(?=")', html).group()
        except:
          video = None
        try:
          html = requests.get(url + "/streams").text
          stream = re.search('(?<="videoId":").*?(?=")', html).group()
        except:
          stream = None

        return {"video":video,"stream":stream}

    async def alert(self,data,t,id):
      channel,guild = await self.get_channel(data["dc_channel"])
      respound = get_respound(guild.preferred_locale,"alert")
      channel_name = Channel.get(data["yt_channel"])["title"]    
      link = "https://www.youtube.com/watch?v="
      await channel.send(respound.get(t).format(channel_name=channel_name,url=link+id))

    @commands.Cog.listener()
    async def on_ready(self):
        # self.check_ytnotificate.start()
        pass

    @tasks.loop(seconds=8,reconnect=True)
    async def check_ytnotificate(self):
        with open("database/notification.json", "r",encoding="utf8") as f:
            database = json.load(f)
        for guild in database:
            channel = list(database[guild].keys())
            for name in channel:
              recent = await self.get_recent_video(database[guild][name]["yt_channel"])
              if database[guild][name]["recent_video"] != recent["video"]:
                database[guild][name]["recent_video"] = recent["video"]
                await self.alert(database[guild][name],"video",recent["video"])
              if database[guild][name]["recent_stream"] != recent["stream"]:
                database[guild][name]["recent_stream"] = recent["stream"]
                await self.alert(database[guild][name],"stream",recent["stream"])
              with open("database/notification.json", "w" ,encoding="utf8") as f:
                  json.dump(database,f,ensure_ascii=False,indent=4)

    @app_commands.command(name="notification",description="notify new uploaded video")
    @app_commands.describe(channel="Channel you wanted to be notice")
    async def youtube_notification(self,interaction:discord.Interaction,channel:str):
      await interaction.response.defer()
      if channel:
        result = Channel.get(channel)
        respound = get_respound(interaction.guild.preferred_locale,"notification")
        embed = discord.Embed(title=result["title"],url=result['url'],description=respound.get("description"),color=0xcc8c2d)
        embed.add_field(name=respound.get("sub"),value=f'`{result["subscribers"]["label"]}`')
        embed.add_field(name=respound.get("view"),value=f'`{result["views"]}`')
        embed.set_thumbnail(url=result['thumbnails'][3]['url'])
        view = check(interaction,channel,self.bot)
        origin = await interaction.followup.send(embed=embed,view=view)
        view.origin = origin
      else:
        await interaction.followup.send("pls try again")
      
    @youtube_notification.autocomplete('channel')
    async def youtube_notification_autocomplete(self,interaction: discord.Interaction,current: str,):
      status = None
      try:
        status = requests.get(current).status_code
      except:pass
      if status  == 200:
        res = requests.get(current)
        res.encoding = "utf-8"
        soup = BeautifulSoup(res.text, 'html.parser')

        link = soup.find_all("link")
        regex = "https://www.youtube.com/channel/"

        for i in link:
            l = i.get('href')
            if l != None:
                if regex in l:
                    s = l[len(regex)-len(l):]
                    data = Channel.get(s)
                    Channelsearch = {'id':data['id'],'subscribers':data['subscribers']['simpleText'],'title':data['title']}
                    break

        sub = "0 subscribers" if Channelsearch["subscribers"] == None else Channelsearch["subscribers"]
        ops = f'{Channelsearch["title"]} | {sub}'
        return [app_commands.Choice(name=ops, value=Channelsearch["id"])]

      else:
        Channelsearch = ChannelsSearch(current,limit =10)
        lst = []
        for channel in Channelsearch.result()["result"]:
                sub = "0 subscribers" if channel['subscribers'] == None else channel["subscribers"]
                ops = f'{channel["title"]} | {sub}'
                lst.append([ops,channel["id"]])
        return [app_commands.Choice(name=l[0], value=l[1])for l in lst]

    @app_commands.command(name="list_notification",description="delete channel in notification list")
    async def list_notification(self,interaction:discord.Interaction):
      await interaction.response.defer()
      with open("database/notification.json", "r",encoding="utf8") as f:
            database = json.load(f)
      pag = []
      number = len(database.get(str(interaction.guild.id)))
      page = math.ceil(number/10)
      if page == 0:
        page = 1
      lists = list(database.get(str(interaction.guild.id)).keys())
      lst = []
      for i in range(number):
          op = f'{i+1}.{lists[i]}'
          lst.append(op)  
      for i in range(page):
          upcoming = list(itertools.islice(lst, 0, 10))
          fmt = '\n'.join(f'**` {_}`**' for _ in upcoming)
          embed = discord.Embed(title="notification list",color = 0xFFFFFF)
          embed.add_field(name = "ในรายการ",value = f'{fmt}',inline = False)
          pag.append(embed) 

      view = buttin(pag,120,interaction)
      await interaction.followup.send(embed = pag[0],view=view)

    @app_commands.command(name="remove_notification",description="Remove given channel from notification list")
    @app_commands.describe(number="Channel Sequence")
    async def remove_notification(self,interaction:discord.Interaction, number:int):
        await interaction.response.defer()
        respound = get_respound(interaction.guild.preferred_locale,"remove_notification")
        with open("database/notification.json", "r",encoding="utf8") as f:
            database = json.load(f)
        if database.get(str(interaction.guild.id)):
          try:
            deleted = list(database[f"{interaction.guild.id}"].keys())[number-1]
          except:
            embed = createembed.remove_error(interaction,self.bot,deleted,respound) 
            await interaction.followup.send(embed=embed)
            await asyncio.sleep(5)
            await d.delete()
            return
          d = await interaction.followup.send(deleted)
          database[str(interaction.guild.id)].pop(deleted)
          with open("database/notification.json", "w" ,encoding="utf8") as f:
                  json.dump(database,f,ensure_ascii=False,indent=4)
          embed = createembed.remove(interaction,self.bot,deleted,respound) 
          await interaction.followup.send(embed=embed)
          await asyncio.sleep(5)
          await d.delete()





async def setup(bot):
  await bot.add_cog(notifyAPI(bot))