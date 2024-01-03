from discord.ext import commands
import json
import discord
from discord import app_commands
import asyncio
from ui.language_respound import get_respound
from ui.embed_gen import createembed
import time
import pymongo

class informationAPI(commands.Cog):
    def __init__(self, bot):
         self.bot = bot

    async def check_ban(self,v):
      if self.bot.mango['ban'].find_one({'user_id':str(v)}):
        return True
      else:
        return False

    @app_commands.command(name="statistic",description="Show statistic of commands usage")
    async def statistic(self,interaction:discord.Interaction): 
        await interaction.response.defer()
        if await self.check_ban(interaction.user.id):
            respound = get_respound(interaction.locale,"baned")
            embed = createembed.baned(interaction,self.bot,respound)
            d = await interaction.followup.send(embed=embed)
            await asyncio.sleep(5)
            await d.delete()
            return
        database = self.bot.mango['Usage_information']
        most = database.find({}).sort('times',pymongo.DESCENDING)[0]
        await interaction.followup.send(f"Mostused: {most['command']} | {most['times']}")
        # await interaction.followup.send("Used: "+used)

    @commands.Cog.listener()
    async def on_app_command_completion(self,interaction, command):
            # await self.update_history(command.name,interaction.user,interaction.guild)
            await self.update_commandused(command.name)
    
    async def update_history(self,command_name:str,user,guild:discord.Guild):
            database = self.bot.mango['Usage_information']
            data = database.find_one({})
            t = time.localtime()
            new = {command_name:f'{user.name}|{guild.name}|{t.tm_mday}/{t.tm_mon}/{t.tm_year}'} 
            if len(data) >= 100:
                del data[-1]
            data[0]["total"] = len(data)
            data.insert(1,new)
            with open("database/Usage_information.json", "w" ,encoding="utf8") as f:
                json.dump(database,f,ensure_ascii=False,indent=2)
        
    async def update_commandused(self,command_name:str):
            database = self.bot.mango['Usage_information']
            data = database.find_one({'command':command_name})
            if not data:
                database.insert_one({
                     'command':command_name,
                     'times':0
                })
            database.update_one({'command':command_name},{'$inc':{f'times':1}})


async def setup(bot):    
  await bot.add_cog(informationAPI(bot))   