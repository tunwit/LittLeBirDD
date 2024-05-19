import discord
from discord import File, Member
from discord.ext import commands,tasks
from discord import app_commands
import asyncio
from ui.embed_gen import createembed
from ui.language_respound import get_respound
from youtubesearchpython import *
from discord.ui import View, Button , button
from ui.button import buttin
import json
from PIL import Image ,ImageDraw ,ImageFont ,ImageOps
import requests
import io
from io import BytesIO
from discord.app_commands import Choice
import time

class welcomeAPI(commands.Cog):
    def __init__(self, bot):
         self.bot = bot

    def finechannel(self,member:discord.Member,channel):
        try:
          channelid = int(channel)
          for channel in member.guild.channels:
            if channel.id == channelid:
                return channel
        except:pass
        return None
    
    async def create_image(self,member:discord.Member,mode,date="21/09/2565"):
      fontname = ImageFont.truetype("WB/Itim Regular.otf", 150)
      fonttime = ImageFont.truetype("WB/Itim Regular.otf", 80)
      img = Image.open(f"WB/{mode}.png")
      txt = Image.new('RGBA', img.size, (255,255,255,0))
      draw = ImageDraw.Draw(txt)

      response = requests.get(member.display_avatar)
      avartar = Image.open(BytesIO(response.content))
      avartar = avartar.resize((650,650))
      mask_im = Image.new("L", avartar.size, 0)
      drawm = ImageDraw.Draw(mask_im)
      drawm.ellipse((0, 0) + avartar.size, fill=255)
      img.paste(avartar, (115, 200), mask_im)
      right_im = 115 + avartar.size[0]
      name = member.name +'#'+member.discriminator
      left = 1310 - fontname.getlength(name)/2
      right = 1310 + fontname.getlength(name)/2

      if left < right_im or right > 1920:
          i = 150
          while left < right_im or right > 1920:
              fontname = ImageFont.truetype("WB/Itim Regular.otf", i)
              i-=1
              left = 1310 - fontname.getlength(name)/2
              right = 1310 + fontname.getlength(name)/2
              
      draw.text((1334, 550),name,(56,77,86,80),font=fontname,anchor='ms',stroke_width=3)
      draw.text((1327, 545),name,(59,79,88,130),font=fontname,anchor='ms',stroke_width=3)
      draw.text((1320, 540),name,(255,255,255),font=fontname,anchor='ms',stroke_width=3)
      draw.text((1320, 660),date,(56,77,86,40),font=fonttime,anchor='ms')
      draw.text((1315, 660),date,(59,79,88,80),font=fonttime,anchor='ms')
      draw.text((1310, 660),date,(255,255,130),font=fonttime,anchor='ms')
      result = Image.alpha_composite(img, txt)
      with io.BytesIO() as welcomecard:
        result.save(welcomecard, 'PNG')
        welcomecard.seek(0)
        return File(fp=welcomecard,filename="welcomcard.png")

    @commands.Cog.listener()
    async def on_member_remove(self,member:discord.Member):
        database = self.bot.mango['welcome']
        data = database.find_one({'guild_id':str(member.guild.id)})
        if data:
          if data["goodbye"]:
            channel_id = data["goodbye"]
            channel = self.finechannel(member,channel_id)
            t = time.localtime()
            file = await self.create_image(member,mode="goodbye",date=f"{t.tm_mday}/{t.tm_mon}/{t.tm_year}")
            await channel.send(f"Goodbye ` {member.name} `, hope to see you again",file=file)

    @commands.Cog.listener()
    async def on_member_join(self,member:discord.Member):
        database = self.bot.mango['welcome']
        data = database.find_one({'guild_id':str(member.guild.id)})
        if data:
          if data["welcome"]:
            channel_id = data["welcome"]
            channel = self.finechannel(member,channel_id)
            t = time.localtime()
            file = await self.create_image(member,mode="welcome",date=f"{t.tm_mday}/{t.tm_mon}/{t.tm_year}")
            await channel.send(f"Welcome {member.mention}, to ` {member.guild.name} ` server!!",file=file)

    @app_commands.command(name="welcomemessage",description="send welcome message to this channel when new user com'in")
    @app_commands.choices(mode=[
  Choice(name = "Welcome",value="welcome"),
  Choice(name = "Goodbye",value="goodbye"),])
    @app_commands.choices(status=[
  Choice(name = "ON",value="ON"),
  Choice(name = "OFF",value="OFF"),])
    async def welcomemessage(self,interaction:discord.Interaction,channel:discord.TextChannel,mode:str,status:str): 
        await interaction.response.defer()
        database = self.bot.mango['welcome']
        data = database.find_one({'guild_id':str(interaction.guild.id)})
        if status == 'ON':
          respound = get_respound(interaction.locale,f"set_{mode}")
          if not data:
            database.insert_one({'guild_id':str(interaction.guild.id),
                              "welcome":None,
                              "goodbye":None})
            
          database.update_one({'guild_id':str(interaction.guild.id)},{'$set':{f'{mode}':str(channel.id)}})
          embed = createembed.set_welcome(interaction,self.bot,respound)
          d = await interaction.followup.send(embed=embed)
          await asyncio.sleep(5)
          await d.delete()
        else:
          respound = get_respound(interaction.locale,f"unset_{mode}")
          if not data:
            embed = createembed.unset_welcome_error(interaction,self.bot,respound)
            d = await interaction.followup.send(embed=embed)
            await asyncio.sleep(5)
            await d.delete()
            return
          
          database.update_one({'guild_id':str(interaction.guild.id)},{'$set':{f'{mode}':None}})       
          fore_data = database.find_one({'guild_id':str(interaction.guild.id)})
          if fore_data["welcome"] == None and fore_data["goodbye"] == None:
              database.delete_one({'guild_id':str(interaction.guild.id)})
          embed = createembed.unset_welcome(interaction,self.bot,respound)
          d = await interaction.followup.send(embed=embed)
          await asyncio.sleep(5)
          await d.delete()

async def setup(bot):    
  await bot.add_cog(welcomeAPI(bot))   