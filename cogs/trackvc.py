import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from ui.embed_gen import createembed
from ui.language_respound import get_respound
import json
from discord.app_commands import Choice

class trackAPI(commands.Cog):
    def __init__(self, bot):
         self.bot = bot

    def finechannel(self,member:discord.Member,channel:str) -> discord.TextChannel:
        try:
          channelid = int(channel)
          for channel in member.guild.channels:
            if channel.id == channelid:
                return channel
        except:pass
        return None

    @app_commands.command(name="trackvc",description="send message when member join or leave vc")
    @app_commands.choices(status=[
  Choice(name = "ON",value="ON"),
  Choice(name = "OFF",value="OFF"),])
    async def track(self,interaction:discord.Interaction,channel:discord.TextChannel,status:str): 
        await interaction.response.defer()
        database = self.bot.mango['trackvc']
        if status == 'ON':
          respound = get_respound(interaction.locale,f"set_track")
          database.insert_one({
              "guild_id":str(interaction.guild.id),
              "text_channel":str(channel.id)
          })
          embed = createembed.set_track(interaction,self.bot,respound,channel.name)
          d = await interaction.followup.send(embed=embed)
          await asyncio.sleep(5)
          await d.delete()
        else:
          respound = get_respound(interaction.locale,f"unset_track")
          if database.find_one({"guild_id":str(interaction.guild.id)}) != None:
            database.delete_one({"guild_id":str(interaction.guild.id)})
          embed = createembed.set_track(interaction,self.bot,respound,channel.name)
          d = await interaction.followup.send(embed=embed)
          await asyncio.sleep(5)
          await d.delete()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member:discord.Member, before, after): 
        database = self.bot.mango['trackvc']
        data = database.find_one({"guild_id":str(member.guild.id)})
        if data == None:
            return
        if member == self.bot.user:
           return
        respound = get_respound(member.guild.preferred_locale,f"trackvc")
        if before.channel == None and after.channel != None: #None -> join
            embed = createembed.joinvc(respound,member,after.channel.name)
        elif before.channel != None and after.channel == None: #Join -> None
            embed = createembed.leavevc(respound,member,before.channel.name)
        elif before.channel != None and after.channel != None and before.channel != after.channel: #Join -> Join (move to)
            embed = createembed.movevc(respound,member,before.channel.name,after.channel.name)
        else:
            return
        channel = self.finechannel(member,data['text_channel'])
        await channel.send(embed=embed)
async def setup(bot):    
  await bot.add_cog(trackAPI(bot))   