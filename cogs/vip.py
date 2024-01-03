from discord.ext import commands
import json
import discord


class vipAPI(commands.Cog):
  def __init__(self, bot):
        self.bot = bot

  async def check_vip(self,v):
      if self.bot.mango['vip'].find_one({'user_id':str(v)}):
        return True
      else:
        return False

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

  @commands.command()
  async def addvip(self, ctx, v):
      await ctx.message.delete()
      database = self.bot.mango['vip']
      data = database.find_one({'user_id':v})
      if not await self.check_dev(ctx.author.id) :
        return
      if data:
        await ctx.send(f'{v} อยู่ในรายการอยู่เเล้ว',delete_after=5)   
        return
      else:
        database.insert_one({'user_id':(v)})
        await ctx.send(f'{v} ถูกเพิ่มในรายการเเล้ว',delete_after=5)


  @commands.command()
  async def removevip(self, ctx, v):
      await ctx.message.delete()
      database = self.bot.mango['vip']
      data = database.find_one({'user_id':v})
      if not await self.check_dev(ctx.author.id) :
        return
      if data:
        database.delete_one({'user_id':v})
        await ctx.send(f'{v} ถูกลบจากรายการเเล้ว',delete_after=5)
        return
      else:
         await ctx.send('สมาชิกนี้ไม่อยู่ในรายการ',delete_after=5)
         return
        
  @commands.command()
  async def checkvip(self, ctx, vip): 
    await ctx.message.delete()
    await ctx.send(await self.check_vip(vip))


  @commands.command()
  async def adddev(self, ctx, v):
      await ctx.message.delete()
      database = self.bot.mango['dev']
      data = database.find_one({'user_id':v})
      if not await self.check_dev(ctx.author.id) :
        return
      if data:
        await ctx.send(f'{v} อยู่ในรายการอยู่เเล้ว',delete_after=5)   
        return
      else:
        database.insert_one({'user_id':(v)})
        await ctx.send(f'{v} ถูกเพิ่มในรายการเเล้ว',delete_after=5)


  @commands.command()
  async def removedev(self, ctx, v):
      await ctx.message.delete()
      database = self.bot.mango['dev']
      data = database.find_one({'user_id':v})
      if not await self.check_dev(ctx.author.id) :
        return
      if data:
        database.delete_one({'user_id':v})
        await ctx.send(f'{v} ถูกลบจากรายการเเล้ว',delete_after=5)
        return
      else:
         await ctx.send('สมาชิกนี้ไม่อยู่ในรายการ',delete_after=5)
         return
        
  @commands.command()
  async def checkdev(self, ctx, dev): 
    await ctx.message.delete()
    await ctx.send(await self.check_vip(dev))

  @commands.command()
  async def addban(self, ctx, v):
      await ctx.message.delete()
      database = self.bot.mango['ban']
      data = database.find_one({'user_id':v})
      if not await self.check_dev(ctx.author.id) :
        return
      if data:
        await ctx.send(f'{v} อยู่ในรายการอยู่เเล้ว',delete_after=5)   
        return
      else:
        database.insert_one({'user_id':(v)})
        await ctx.send(f'{v} ถูกเพิ่มในรายการเเล้ว',delete_after=5)


  @commands.command()
  async def removeban(self, ctx, v):
      await ctx.message.delete()
      database = self.bot.mango['ban']
      data = database.find_one({'user_id':v})
      if not await self.check_dev(ctx.author.id) :
        return
      if data:
        database.delete_one({'user_id':v})
        await ctx.send(f'{v} ถูกลบจากรายการเเล้ว',delete_after=5)
        return
      else:
         await ctx.send('สมาชิกนี้ไม่อยู่ในรายการ',delete_after=5)
         return
        
  @commands.command()
  async def checkban(self, ctx, ban): 
    await ctx.message.delete()
    await ctx.send(await self.check_vip(ban))
    
async def setup(bot):    
  await bot.add_cog(vipAPI(bot))   