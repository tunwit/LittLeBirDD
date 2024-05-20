import discord
from discord.ext import commands
import json
from discord import app_commands
from discord.app_commands import Choice
import asyncio
from ui.language_respound import get_respound
from ui.embed_gen import createembed

class serverstatsAPI(commands.Cog):
  def __init__(self,bot):
     self.bot = bot
     self.category = "📃 สถานะเซิร์ฟเวอร์ 📃"

  async def check_ban(self,v):
      if self.bot.mango['ban'].find_one({'user_id':str(v)}):
        return True
      else:
        return False

  def finechannel(self,interacion,channel):
    try:
      channelid = int(channel)
      for channel in interacion.guild.channels:
        if channel.id == channelid:
            return channel
    except:pass
    return None

  @commands.Cog.listener()
  async def on_member_join(self,message):
    database = self.bot.mango['serverstate']
    serverstat = database.find_one({'guild_id':str(message.guild.id)})
    if not serverstat:
      return
    respound = get_respound(message.guild.preferred_locale,"setup_stats")
    channel = self.finechannel(message,serverstat['allmember'])
    try:
     await channel.edit(name = f'{respound.get("allmember")} | {message.guild.member_count}')
    except: pass
    channel = self.finechannel(message,serverstat['user_channel'])
    try:
     await channel.edit(name = f'{respound.get("user")} | {len([m for m in message.guild.members if not m.bot])}')
    except: pass
    channel = self.finechannel(message,serverstat['bot'])
    try:
     await channel.edit(name = f'{respound.get("bot")} | {len([m for m in message.guild.members if m.bot])}')
    except: pass
    
  @commands.Cog.listener()
  async def on_member_remove(self,message:discord.Member):
    database = self.bot.mango['serverstate']
    serverstat = database.find_one({'guild_id':str(message.guild.id)})
    if not serverstat:
      return
    respound = get_respound(message.guild.preferred_locale,"setup_stats")
    channel = self.finechannel(message,serverstat['allmember'])
    try:
     await channel.edit(name = f'{respound.get("allmember")} | {message.guild.member_count}')
    except: pass
    channel = self.finechannel(message,serverstat['user_channel'])
    try:
     await channel.edit(name = f'{respound.get("user")} | {len([m for m in message.guild.members if not m.bot])}')
    except: pass
    channel = self.finechannel(message,serverstat['bot'])
    try:
     await channel.edit(name = f'{respound.get("bot")} | {len([m for m in message.guild.members if m.bot])}')
    except: pass

  @app_commands.command(name="reset_stats",description="Delete member count channel")
  async def reset_stats(self,interaction:discord.Interaction):
    await interaction.response.defer()
    if await self.check_ban(interaction.user.id):
        respound = get_respound(interaction.locale,"baned")
        embed = createembed.embed_fail(interaction,respound)
        d = await interaction.followup.send(embed=embed)
        await asyncio.sleep(5)
        await d.delete()
        return
    respound = get_respound(interaction.locale,'reset_stats')
    database = self.bot.mango['serverstate']
    server = database.find_one({'guild_id':str(interaction.guild.id)})
    if not server:
      embed = createembed.embed_fail(interaction,respound)
      d = await interaction.followup.send(embed=embed)  
      await asyncio.sleep(5)
      await d.delete()
      return
    server.pop('_id')
    for i in list(server):
      channel = self.finechannel(interaction,int(server[i]))
      try:
         await channel.delete()
      except:pass
    embed = createembed.embed_success(interaction,respound)
    database.delete_one({'guild_id':str(interaction.guild.id)})
    d = await interaction.followup.send(embed=embed)
    await asyncio.sleep(5)
    await d.delete()

  @app_commands.command(name="setup_stats",description="Create member count channel")
  @app_commands.checks.has_permissions(administrator=True)
  @app_commands.describe(type="Type of channel")
  @app_commands.choices(type=[
    Choice(name = "Voice (Recommended)",value="voice"),
    Choice(name = "Text",value="Text")])   
  async def setup_stats(self,interaction:discord.Interaction,type:str):
    await interaction.response.defer()
    if await self.check_ban(interaction.user.id):
        respound = get_respound(interaction.locale,"baned")
        embed = createembed.embed_fail(interaction,respound)
        d = await interaction.followup.send(embed=embed)
        await asyncio.sleep(5)
        await d.delete()
        return
    respound = get_respound(interaction.locale,'setup_stats')
    database = self.bot.mango['serverstate']
    server = database.find_one({'guild_id':str(interaction.guild.id)})
    if server:
      embed = createembed.embed_fail(interaction,respound)
      d = await interaction.followup.send(embed=embed)   
      await asyncio.sleep(5)
      await d.delete()
      return
    elif type == "voice":
      category = await interaction.guild.create_category(self.category, position=0)
      allmember = await interaction.guild.create_voice_channel(f'{respound.get("allmember")} | {interaction.guild.member_count}',category=category)
      await allmember.set_permissions(interaction.guild.default_role, connect=False)
      user = await interaction.guild.create_voice_channel(f'{respound.get("user")} | {len([m for m in interaction.guild.members if not m.bot])}',category=category)
      await user.set_permissions(interaction.guild.default_role, connect=False)
      botc = await interaction.guild.create_voice_channel(f'{respound.get("bot")} | {len([m for m in interaction.guild.members if m.bot])}',category=category)
      await botc.set_permissions(interaction.guild.default_role, connect=False)
    elif type == "text":
      category = await interaction.guild.create_category(self.category, position=0)
      allmember = await interaction.guild.create_text_channel(f'{respound.get("allmember")}|{interaction.guild.member_count}',category=category)
      await allmember.set_permissions(interaction.guild.default_role, send_messages=False)
      user = await interaction.guild.create_text_channel(f'{respound.get("user")}|{len([m for m in interaction.guild.members if not m.bot])}',category=category)
      await user.set_permissions(interaction.guild.default_role, send_messages=False)
      botc = await interaction.guild.create_text_channel(f'{respound.get("bot")}|{len([m for m in interaction.guild.members if m.bot])}',category=category)
      await botc.set_permissions(interaction.guild.default_role, send_messages=False)
    
    database.insert_one({
      'guild_id':str(interaction.guild.id),
      "allmember":allmember.id,
      "bot":botc.id,
      "user_channel":user.id,
      "category":category.id
    })
    embed = createembed.embed_success(interaction,respound)
    d = await interaction.followup.send(embed=embed)
    await asyncio.sleep(5)
    await d.delete()
  
  @setup_stats.error
  async def setup_statsError(self,interaction:discord.Interaction,error:app_commands.AppCommandError):
    if isinstance(error,app_commands.MissingPermissions):
      await interaction.response.defer()
      respound = get_respound(interaction.locale,"setup_statsError")
      embed = createembed.embed_fail(interaction,respound)
      d = await interaction.followup.send(embed=embed)   
      await asyncio.sleep(5)
      await d.delete()
    else:
      raise error
      
    
async def setup(bot):
  await bot.add_cog(serverstatsAPI(bot))