import discord
from discord.ext import commands
import json
import lyricsgenius
import asyncio
import wavelink
from discord import app_commands
from discord.app_commands import Choice
from ui.language_respound import get_respound
from ui.embed_gen import createembed
from config import LYRICSGENIUS
#---------------------------------------- on_ready
class Bot(commands.Cog):
  def __init__(self, bot:commands.bot):
    self.bot = bot
    self.msg = {}
    self.lymsg = {}
    self.genius = lyricsgenius.Genius(LYRICSGENIUS)

  async def check_dev(self,v):
      if self.bot.mango['dev'].find_one({'user_id':str(v)}):
        return True
      else:
        return False
        
  async def check_ban(self,v):
      if self.bot.mango['ban'].find_one({'user_id':str(v)}):
        return True
      else:
        return False

  @commands.Cog.listener()
  async def on_guild_join(self,guild:discord.Guild):
      respound = get_respound(guild.preferred_locale,"welcome")
      for channel in guild.text_channels:
          await channel.send(respound.get("wel"),delete_after = 60)
          break

  #----------------------------------------------- other
  @app_commands.command(name="lyrics",description="Find lyrics given music")
  @app_commands.describe(search="Song name")
  async def lyrics(self,interaction:discord.Interaction, search:str):  
    await interaction.response.defer()
    if await self.check_ban(interaction.user.id):
      respound = get_respound(interaction.locale,"baned")
      embed = createembed.baned(interaction,interaction.client,respound)
      d = await interaction.followup.send(embed=embed)
      await asyncio.sleep(5)
      await d.delete()
      return

    respound = get_respound(interaction.locale,"lyrics")
    search = self.genius.search_song(search)
    if search == None:
      embed = createembed.lyrics(interaction,interaction.client,respound)
      d = await interaction.followup.send(embed=embed)
      await asyncio.sleep(5)
      await d.delete()
    data = self.genius.song(search.id)
    embed = discord.Embed(title=data['song']['title'],description=search.lyrics,colour= interaction.user.colour)
    embed.set_thumbnail(url=data['song']['song_art_image_url'])
    embed.set_author(name=data['song']['artist_names'])
    if interaction.guild.id in self.lymsg :
       await self.lymsg[interaction.guild.id].delete()   
    id = await interaction.followup.send(embed=embed)
    self.lymsg[interaction.guild.id] = id
    await self.lymsg[interaction.guild.id].add_reaction('❌')
    
  @commands.Cog.listener()
  async def on_reaction_add(self,reaction, user):
      if user == self.bot.user:
        return
      else:
        try:
         if reaction.message.id == self.lymsg[user.guild.id].id:
            if reaction.emoji =='❌':
              await reaction.remove(user)
              await self.lymsg[user.guild.id].delete()
        except:return

  @commands.command()
  async def checkplay(self,ctx):
    await ctx.message.delete()
    if not await self.check_dev(ctx.author.id) :
      return
    embed = discord.Embed(title = f'Here is player status in {len(self.bot.guilds)} server',color=0x53BD40 ) 
    i = 0
    for guild in self.bot.guilds:
        vc: wavelink.Player = guild.voice_client
        try:
          if vc.is_connected():
            embed.add_field(name= guild.name, value = "Playing",inline=False)
            i += 1
        except:
            embed.add_field(name= guild.name, value = "Not play",inline=False)
    embed.set_footer(text = f"There is {i} servers using bot", icon_url=ctx.author.avatar.url)  
    i = 0 
    await ctx.send(embed = embed,delete_after = 25)   
    
  # @app_commands.command(name="prefix_change",description="Change prefix for your server")
  # @app_commands.describe(prefix="Prefix you wanted")
  # async def changeprefix(self,interaction:discord.Interaction,prefix:str):
  #   await interaction.response.defer()
  #   prefixs = await self.bot.pg_con.fetchrow("SELECT * FROM prefixs WHERE guild_id = $1",str(interaction.guild.id)) 
  #   if not prefixs:
  #     await self.bot.pg_con.execute("INSERT INTO prefixs (guild_id,prefix) VALUES ($1,$2)",str(interaction.guild.id),prefix)
  #   else:
  #     await self.bot.pg_con.execute("UPDATE prefixs SET prefix = $1 WHERE guild_id = $2",prefix,str(interaction.guild.id))
  #   prefix = await self.get_prefix(interaction)
  #   if await self.get_lange(interaction) == 'th':
  #     cpembed=discord.Embed(title=f"{self.bot.user.name} | Prefixchanged ❗️❗️",description=f"เซิร์ฟเวอร์ {interaction.guild.name} ได้เปลี่ยนprefixเป็น **``{prefix}``** เเล้วคะ",color=0x36FF00)
  #     cpembed.set_footer(text = f"สำหรับเซิร์ฟเวอร์{interaction.guild.name}ใช้เครื่องหมาย {prefix} เเล้วตามด้วยคำสั่งนะคะ", icon_url=interaction.user.avatar.url)
  #   elif await self.get_lange(interaction) == 'en': 
  #     cpembed=discord.Embed(title=f"{self.bot.user.name} | Prefixchanged ❗️❗️",description=f"Server {interaction.guild.name} the prefix has changed to **``{prefix}``** ",color=0x36FF00)
  #     cpembed.set_footer(text = f"For server {interaction.guild.name} use {prefix} and follow by the commands", icon_url=interaction.user.avatar.url)
  #   d = await interaction.followup.send(embed=cpembed)
  #   await asyncio.sleep(5)
  #   await d.delete()

  # @app_commands.command(name="language_change",description="Change language for your server")
  # @app_commands.describe(language="Language you wanted")
  # @app_commands.choices(language=[
  #   Choice(name = "EN",value="en"),
  #   Choice(name = "TH",value="th")])
  # async def lang(self,interaction:discord.Interaction,language:str):
  #   await interaction.response.defer()
  #   prefix = await self.get_prefix(interaction)
  #   langs = await self.bot.pg_con.fetchrow("SELECT * FROM language WHERE guild_id = $1" ,str(interaction.guild.id))
  #   if not langs:
  #     await self.bot.pg_con.execute("INSERT INTO language (guild_id,lang) VALUES ($1,$2)",str(interaction.guild.id),language)
  #   else:
  #     await self.bot.pg_con.execute("UPDATE language SET lang = $1 WHERE guild_id = $2",language,str(interaction.guild.id))
  #   if await self.get_lange(interaction) == 'th':
  #     embed = discord.Embed(title=f'{self.bot.user.name} | เปลี่ยนภาษาเเล้ว ✅', description=f"ตอนนี้เปลี่ยนภาษาเป็น **`TH`** เเล้วคะ",color=0x19AD3B)
  #     embed.set_footer(text = f"สำหรับเซิร์ฟเวอร์{interaction.guild.name}ใช้เครื่องหมาย {prefix} เเล้วตามด้วยคำสั่งนะคะ", icon_url=interaction.user.avatar.url)
  #   elif await self.get_lange(interaction) == 'en':
  #     embed = discord.Embed(title=f'{self.bot.user.name} | Language changed ✅', description=f"Language is now **`En`** ",color=0x19AD3B)
  #     embed.set_footer(text = f"For server {interaction.guild.name} use {prefix} and follow by the commands", icon_url=interaction.user.avatar.url)
  #   d = await interaction.followup.send(embed=embed)
  #   await asyncio.sleep(5)
  #   await d.delete()

  @commands.command()
  async def serverlist(self,ctx):
   await ctx.message.delete()
   if not await self.check_dev(ctx.author.id) :
      return
   embed = discord.Embed(title = f'Now bot are in {len(self.bot.guilds)} server',color=0x53BD40 ) 
   for guild in self.bot.guilds:
          embed.add_field(name= guild.name, value = guild.id,inline=False)
   await ctx.send(embed = embed,delete_after = 10)
   
  
  @app_commands.command(name="ping",description="response with pong!! and latency")
  async def ping(self,interaction:discord.Interaction):
    if await self.check_ban(interaction.user.id):
      respound = get_respound(interaction.locale,"baned")
      embed = createembed.baned(interaction,interaction.client,respound)
      d = await interaction.followup.send(embed=embed)
      await asyncio.sleep(5)
      await d.delete()
      return    
    await interaction.response.send_message(f'Pong!! Latency:{self.bot.latency}ms')

  
async def setup(bot):
  await bot.add_cog(Bot(bot))

