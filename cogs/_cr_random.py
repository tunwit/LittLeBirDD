import discord
from discord.ext import commands
import random
import json
from discord import app_commands
import asyncio
from ui.embed_gen import createembed
from ui.language_respound import get_respound

class randomAPI(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  async def check_ban(self,v):
      if self.bot.mango['ban'].find_one({'user_id':v}):
        return True
      else:
        return False

  @app_commands.command(name="custom_random",description="Activate recive options function")
  async def cr(self,interaction:discord.Interaction):
    await interaction.response.defer()
    if await self.check_ban(interaction.user.id):
      respound = get_respound(interaction.locale,"baned")
      embed = createembed.baned(interaction,interaction.client,respound)
      d = await interaction.followup.send(embed=embed)
      await asyncio.sleep(5)
      await d.delete()
      return
    with open("database/customrandom.json", "r",encoding="utf8") as f:
        database = json.load(f)
    respound = get_respound(interaction.locale,"cr")
    i=0
    while True:
      i+=1
      m1 = await interaction.followup.send(respound.get('activatechoice').format(i=i))
      def check(m):
        return m.author.id == interaction.user.id
      message = await self.bot.wait_for("message", check=check)
      await m1.delete()
      if message.content == "!?":
        with open("database/customrandom.json", "w" ,encoding="utf8") as f:
          json.dump(database,f,ensure_ascii=False,indent=4)
        d = await interaction.followup.send(respound.get('deactivatechoice'))
        await message.delete()
        await asyncio.sleep(5)
        await d.delete()
        return

      choice = message.content
      g = database.get(str(interaction.guild.id),None)
      if not g:
        database[f"{str(interaction.guild.id)}"] = [choice]
      else:
        database[f"{str(interaction.guild.id)}"].append(choice)
      await message.delete()
      
  @app_commands.command(name="cr_random",description="Random option(s) list")
  async def cr_random(self,interaction:discord.Interaction):
    await interaction.response.defer()
    if await self.check_ban(interaction.user.id):
      respound = get_respound(interaction.locale,"baned")
      embed = createembed.baned(interaction,interaction.client,respound)
      d = await interaction.followup.send(embed=embed)
      await asyncio.sleep(5)
      await d.delete()
      return
    with open("database/customrandom.json", "r",encoding="utf8") as f:
        database = json.load(f)
    respound = get_respound(interaction.locale,"cr")
    randomc = database.get(str(interaction.guild.id),None)
    if not randomc:
        embed = createembed.cr_randomnolist(interaction,self.bot,respound)      
        d = await interaction.followup.send(embed=embed)
        await asyncio.sleep(5)
        await d.delete()
        return
    d = await interaction.followup.send(random.choice(randomc))
    await asyncio.sleep(15)
    await d.delete()
#-------------------------------------------------
    
  @app_commands.command(name="cr_clear",description="Delete all options in list")
  async def cr_clear(self,interaction:discord.Interaction):
    await interaction.response.defer()
    if await self.check_ban(interaction.user.id):
      respound = get_respound(interaction.locale,"baned")
      embed = createembed.baned(interaction,interaction.client,respound)
      d = await interaction.followup.send(embed=embed)
      await asyncio.sleep(5)
      await d.delete()
      return
    with open("database/customrandom.json", "r",encoding="utf8") as f:
        database = json.load(f)
    respound = get_respound(interaction.locale,"cr_clear")
    database.pop(str(interaction.guild.id))
    embed = createembed.cr_clearsuccess(interaction,self.bot,respound)
    with open("database/customrandom.json", "w" ,encoding="utf8") as f:
          json.dump(database,f,ensure_ascii=False,indent=4)         
    d = await interaction.followup.send(embed=embed)
    await asyncio.sleep(15)
    await d.delete()

  @app_commands.command(name="cr_list",description="Send option(s)list")
  async def cr_list(self,interaction:discord.Interaction):
    await interaction.response.defer()
    if await self.check_ban(interaction.user.id):
      respound = get_respound(interaction.locale,"baned")
      embed = createembed.baned(interaction,interaction.client,respound)
      d = await interaction.followup.send(embed=embed)
      await asyncio.sleep(5)
      await d.delete()
      return
    with open("database/customrandom.json", "r",encoding="utf8") as f:
        database = json.load(f)
    respound = get_respound(interaction.locale,"cr_list")
    randomc = database.get(str(interaction.guild.id),None)
    if not randomc or len(randomc) == 0:
      embed = createembed.cr_listnolist(interaction,self.bot,respound)         
      d = await interaction.followup.send(embed=embed)
      await asyncio.sleep(15)
      await d.delete()
      return
    embed = discord.Embed(title=respound.get("num").format(x=len(randomc)), description="lists",color=0x269BCE)
    for i in range(len(randomc)):
      embed.add_field(name=randomc[i], value=i+1,inline=False)
      embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
    d = await interaction.followup.send(embed=embed)
    await asyncio.sleep(15)
    await d.delete()

  @app_commands.command(name="cr_remove",description="Remove given option")
  @app_commands.describe(number="Option squence")
  async def cr_remove(self,interaction:discord.Interaction,number:int):
    await interaction.response.defer()
    if await self.check_ban(interaction.user.id):
      respound = get_respound(interaction.locale,"baned")
      embed = createembed.baned(interaction,interaction.client,respound)
      d = await interaction.followup.send(embed=embed)
      await asyncio.sleep(5)
      await d.delete()
      return
    with open("database/customrandom.json", "r",encoding="utf8") as f:
        database = json.load(f)
    respound = get_respound(interaction.locale,"cr_remove")
    randomc = database.get(str(interaction.guild.id),None) 
    if not randomc or len(randomc) == 0:
      embed = createembed.cr_removefailed(interaction,self.bot,respound)         
      d = await interaction.followup.send(embed=embed)
      await asyncio.sleep(15)
      await d.delete()
      return
    deleted = randomc[number-1]
    del database.get(str(interaction.guild.id),None) [number-1]
    d = await interaction.followup.send(respound.get("deleted").format(deleted=deleted))
    with open("database/customrandom.json", "w" ,encoding="utf8") as f:
          json.dump(database,f,ensure_ascii=False,indent=4)   
    await asyncio.sleep(15)
    await d.delete()

async def setup(bot):
  await bot.add_cog(randomAPI(bot))
       
    

 




        

       
