import discord
from discord.ext import commands
import json
from discord import app_commands
import asyncio
from ui.embed_gen import createembed
from ui.language_respound import get_respound

class userstateAPI(commands.Cog):
  def __init__(self,bot):
     self.bot = bot
     self.cd = commands.CooldownMapping.from_cooldown(1, 25, commands.BucketType.user)
     self.uprate = 7
     self.require_exp = 500

  async def check_ban(self,v):
      if self.bot.mango['ban'].find_one({'user_id':str(v)}):
        return True
      else:
        return False

  def ratelimit_check(self, message):
        """Returns the ratelimit left"""
        bucket = self.cd.get_bucket(message)
        return bucket.update_rate_limit()
        
  async def toggle(self,message):
      database = self.bot.mango['toggle']
      data = database.find_one({'guild_id':str(message.guild.id)})
      if not data:
        database.insert_one({
           "guild_id":str(message.guild.id),
           "status":False
        })
      if not data:
        return False
      else:
        return True
    
  @commands.Cog.listener()
  async def on_message(self,message):
    if message.author.bot:
      return
    if self.ratelimit_check(message) == None:
      if await self.toggle(message) == True:
        await self.update_data(message)
        await self.add_exp(message)
        await self.detact_levelup(message)
    return
  
  async def update_data(self,message:discord.Message):
      database = self.bot.mango['level']
      try:
        key = str(message.author.id)+str(message.guild.id)
      except:
        key = str(message.user.id)+str(message.guild.id)
      user = database.find_one({'key_id':str(key)})
      if not user:
        try:
          database.insert_one({
           "key_id":key,
           "user_id":str(message.author.id),
           "guild_id":str(message.guild.id),
           "level":1,
           "exp":0
        })
        except:
          database.insert_one({
           "key_id":key,
           "user_id":str(message.user.id),
           "guild_id":str(message.guild.id),
           "level":1,
           "exp":0
        })

  async def add_exp(self,message):
     database = self.bot.mango['level']
     key = str(message.author.id)+str(message.guild.id)
     database.update_one({'key_id':key},{'$inc':{f'exp':self.uprate}})

  async def detact_levelup(self,message):
     database = self.bot.mango['level']
     key = str(message.author.id)+str(message.guild.id)
     level = database.find_one({
        'key_id':key,
     })
     respound = get_respound(message.guild.preferred_locale,"detact_levelup")
     if level['exp'] >= self.require_exp:
        database.update_one({'key_id':key},{'$inc':{f'level':1}})
        database.update_one({'key_id':key},{'$set':{f'exp':0}})
        await message.channel.send(respound.get("descript").format(mention=message.author.mention,level=level['level']),delete_after = 8)

  @app_commands.command(name="toggle_level",description="To turn on/off level system")
  async def toggle_lv(self,interaction:discord.Interaction):
    await interaction.response.defer()
    if await self.check_ban(interaction.user.id):
        respound = get_respound(interaction.locale,"baned")
        embed = createembed.baned(interaction,interaction.client,respound)
        d = await interaction.followup.send(embed=embed)
        await asyncio.sleep(5)
        await d.delete()
        return
    database = self.bot.mango['toggle']
    toggle = database.find_one({'guild_id':str(interaction.guild.id)})
    if toggle['status'] == True:
      database.update_one({'guild_id':str(interaction.guild.id)},{'$set':{f'status':False}})
    elif toggle['status'] == False:
      database.update_one({'guild_id':str(interaction.guild.id)},{'$set':{f'status':True}})
    final = database.find_one({'guild_id':str(interaction.guild.id)})
    respound = get_respound(interaction.locale,"toggle_lv")
    embed = createembed.toggle_lv(interaction,self.bot,final['status'],respound)   
    d = await interaction.followup.send(embed=embed)
    await asyncio.sleep(5)
    await d.delete()

  @app_commands.command(name="level",description="Send your current level and exp")
  async def lv(self,interaction:discord.Interaction): 
    await interaction.response.defer()
    if await self.check_ban(interaction.user.id):
        respound = get_respound(interaction.locale,"baned")
        embed = createembed.baned(interaction,interaction.client,respound)
        d = await interaction.followup.send(embed=embed)
        await asyncio.sleep(5)
        await d.delete()
        return
    key = str(interaction.user.id)+str(interaction.guild.id)
    database = self.bot.mango['level']
    data = database.find_one({'key_id':key})
    respound = get_respound(interaction.locale,"lv")
    await self.update_data(interaction)
    d = await interaction.followup.send(respound.get("descript").format(mention=interaction.user.mention,level=data['level'],exp=data['exp'],percantage=round((data['exp']/500)*100)))
    await asyncio.sleep(8)
    await d.delete()

async def setup(bot):
  await bot.add_cog(userstateAPI(bot))
  