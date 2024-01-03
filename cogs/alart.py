import discord
from discord.ext import commands,tasks
from discord_together import DiscordTogether
import json
from discord import app_commands
from discord.app_commands import Choice
import asyncio
from ui.language_respound import get_respound
from ui.help_embed import embed
from ui.button import buttin
from ui.embed_gen import createembed
from datetime import datetime,timedelta
from typing import Optional

class alart(commands.Cog):
    def __init__(self, bot:commands.bot):
        self.bot = bot

    async def check_ban(self,v):
        if self.bot.mango['ban'].find_one({'user_id':str(v)}):
            return True
        else:
            return False

    
    @tasks.loop(seconds=2)
    async def notify(self):
        database = self.bot.mango['reminder']
        ob:dict = database.find({}) 
        for event in ob:
            now = datetime.now()
            target_time = event['time'] 
            if now >=target_time:
                if (now - target_time) > timedelta(days=1):
                    database.delete_one({'_id':event.get('_id')})
                    break
                user_id = event.get('user_id')
                user:discord.User = self.bot.get_user(int(user_id)) 
                channel_id = event.get('channel_id')
                if channel_id:
                    channel:discord.TextChannel = self.bot.get_channel(int(event['channel_id']))
                    respound = get_respound(channel.guild.preferred_locale,"reminder")
                    embed = createembed.reminder(user,self.bot,respound,event.get('message'))
                    await channel.send(embed=embed)
                    database.delete_one({'_id':event.get('_id')})
                    break
                elif not channel_id :
                    respound = get_respound("en-US","reminder")
                    embed = createembed.reminder(user,self.bot,respound,event.get('message'))
                    await user.send(embed=embed)
                    database.delete_one({'_id':event.get('_id')})
                    break

    @commands.Cog.listener()
    async def on_ready(self):
        self.notify.start()

    @app_commands.command(name="reminder",description="to send you a message to remind you of smth")
    @app_commands.describe(date="set the date send you a message (1-31)")
    @app_commands.describe(month="set the month send you a message")
    @app_commands.describe(year="set the year send you a message (only B.C.)")
    @app_commands.describe(time="set the time in 24 system send you a message (hh:mm)")
    @app_commands.describe(message="a message to send to remind you")
    @app_commands.describe(via="how the bot will send you a message")
    @app_commands.choices(via=[
    Choice(name = "DM (Direct Message)",value="dm"),
    Choice(name = "This channel",value="channel")])
    @app_commands.choices(month=[Choice(name = f"{str(month[0]).zfill(2)} | {month[1]}",value=str(month[0])) for month in enumerate([
  "January", "February", "March", "April",
  "May", "June", "July", "August",
  "September", "October", "November", "December"
],start=1)])
    async def reminder(self,interaction:discord.Interaction,message:str,date:str,month:str,year:str,time:str,via:str):
        await interaction.response.defer()
        if await self.check_ban(interaction.user.id):
            respound = get_respound(interaction.locale,"baned")
            embed = createembed.baned(interaction,interaction.client,respound)
            d = await interaction.followup.send(embed=embed)
            await asyncio.sleep(5)
            await d.delete()
            return
        
        date_string = f"{year}-{month}-{date} {time}"
        input_format = "%Y-%m-%d %H:%M"
        try:
            datetime_object = datetime.strptime(date_string, input_format)
        except ValueError:
            respound = get_respound(interaction.locale,"invalid_format")
            embed = createembed.invalid_format(interaction,interaction.client,respound)
            d = await interaction.followup.send(embed=embed)
            await asyncio.sleep(5)
            await d.delete()
            return

        if datetime.now() > datetime_object:
            respound = get_respound(interaction.locale,"invalid_format")
            embed = createembed.foretime(interaction,interaction.client,respound)
            d = await interaction.followup.send(embed=embed)
            await asyncio.sleep(5)
            await d.delete()
            return
        
        database = self.bot.mango['reminder']
        channel = None
        if via == 'channel':
            channel = str(interaction.channel.id)
        database.insert_one({   
            'user_id':str(interaction.user.id),
            'message':message,
            'time':datetime_object,
            'channel_id':channel
             })
        respound = get_respound(interaction.locale,"reminder")
        embed = createembed.set_reminder_com(interaction,interaction.client,respound,_time=datetime_object,message=message)
        d = await interaction.followup.send(embed=embed)
        await asyncio.sleep(5)
        await d.delete()

async def setup(bot):    
  await bot.add_cog(alart(bot))        
