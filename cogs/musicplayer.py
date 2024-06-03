from typing import List, Optional
import discord
from discord.ext import commands
import wavelink
import asyncio
import json
from async_timeout import timeout
import math
import itertools
from cogs.createsource import createsource
import random
from discord.ui import Button, View
from discord import app_commands
from discord.app_commands import Choice
from spotipy_random import get_random
import random
from ui.embed_gen import createembed
from ui.language_respound import get_respound
from ui.button import buttin
from ui.controlpanal import *
import requests
import random
import os
import datetime
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import datetime
from urllib.parse import urlparse
from PIL import Image, ImageDraw 
import io
import logging
from config import CLIENT_ID,CLIENT_SECRET
import sys
logger = logging.getLogger('littlebirdd')

def unhandle_exception(exc_type, exc_value, exc_traceback):
    logger = logging.getLogger('littlebirdd')
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = unhandle_exception
trans_queueMode= {
            'wavelink.QueueMode.normal':"Disable",
            'wavelink.QueueMode.loop':"Song",
            'wavelink.QueueMode.loop_all':"Queue"
        }

trans_autoMode= {
            'wavelink.AutoPlayMode.partial':"Disable",
            'wavelink.AutoPlayMode.enabled':"Enable"
        }

def convert(milliseconds):
    seconds = milliseconds // 1000  # Convert milliseconds to seconds
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)


async def check_before_play(interaction: discord.Interaction):
    vc: wavelink.Player = interaction.guild.voice_client
    respound = get_respound(interaction.locale, "check_before_play")
    if vc == None:
        embed = createembed.embed_fail(interaction,respound['novc'])
        await interaction.followup.send(embed=embed, ephemeral=True)
        return False
    if interaction.user.voice == None:
        embed = createembed.embed_fail(interaction,respound['usernotin'])
        await interaction.followup.send(embed=embed, ephemeral=True)
        return False
    if interaction.guild.voice_client.channel != interaction.user.voice.channel:
        embed = createembed.embed_fail(interaction,respound['diffchan'])
        await interaction.followup.send(embed=embed, ephemeral=True)
        return False
    return True


class nowplaying: 

    async def np(self,interaction, send=False):
            vc: wavelink.Player = interaction.guild.voice_client
            respound = get_respound(interaction.locale, "np")
            if vc:
                if vc.current is not None:
                    lst = list(vc.queue)
                    if vc.queue.mode == wavelink.QueueMode.loop_all:
                        lst = lst +list(vc.queue.history)
                    upcoming = list(itertools.islice(lst,0, 4))
                    fmt = "\n".join(
                        f'` {index}.{track} `' for index,track in enumerate(upcoming,start=1)  
                    )    
                    try:
                        duration = f"{convert(vc.position)}/{convert(vc.current.length)}"
                    except:
                        duration = respound.get("unable_duration")
                    npembed = discord.Embed(
                        title=f"{vc.current.title}  <a:blobdancee:969575788389220392>",
                        url=vc.current.uri,
                        color=0xFFFFFF,
                    )
                    npembed.set_author(
                        name=f"{respound.get('addedby')} {vc.current.extras.requester}",
                        icon_url=f"{vc.current.extras.requester_icon}",
                    )
                    npembed.add_field(
                        name=f"{respound.get('playingin')}", value=f"<#{vc.channel.id}>"
                    )
                    npembed.add_field(
                        name=f"{respound.get('duration')}", value=f"`{duration}`"
                    )
                    npembed.set_footer(
                        text=f"{'Paused'if vc.paused else 'Playing'} | {vc.volume}% | LoopStatus:{trans_queueMode[f'wavelink.{str(vc.queue.mode)}']} | Autoplay:{trans_autoMode[f'wavelink.{str(vc.autoplay)}']}"
                    )
                    npembed.set_thumbnail(url=vc.current.artwork)
                    more = f"`{respound.get('andmore').format(more=len(lst)-4)}`"
                    if len(lst) - 4 <= 0:
                        more = None
                    if len(fmt) == 0:
                        fmt = f"`{respound.get('fmt')}`"
                    with io.BytesIO() as image_binary:
                        total = vc.current.length // 1000
                        progress = vc.position // 1000
                        w, h =  350, 10
                        r=3
                        length = (progress*w)/total
                        img = Image.new("RGBA", (w, h)) 
                        img1 = ImageDraw.Draw(img)   
                        img1.line(xy=(-1,5,350,5),fill ="white",width=2) 
                        img1.line(xy=(-1,5,length,5),fill ="red",width=2,joint='curve')
                        img1.ellipse(xy=(length-r,5-r,length+r,5+r) ,fill='darkred')
                        img.save(image_binary,'PNG')
                        image_binary.seek(0)

                        file = discord.File(image_binary, filename="image.png")
                        
                        npembed.set_image(url="attachment://image.png")
                        if send:
                            content = f'**{respound.get("queue")}:**\n{fmt}'f'\n{more}' if more else f'**{respound.get("queue")}:**\n{fmt}'
                            vc.np = await vc.interaction.followup.send(content=content, embed=npembed,view=vc.Myview ,file=file)
                            return
                        if vc.np:
                            try:
                                content = f'**{respound.get("queue")}:**\n{fmt}'f'\n{more}' if more else f'**{respound.get("queue")}:**\n{fmt}'
                                vc.np = await vc.interaction.followup.edit_message(message_id=vc.np.id,content=content, embed=npembed,view=vc.Myview ,attachments=[file])
                            except:
                                content = f'**{respound.get("queue")}:**\n{fmt}'f'\n{more}' if more else f'**{respound.get("queue")}:**\n{fmt}'
                                vc.np = await vc.interaction.followup.edit_message(message_id=vc.np.id,content=content, embed=npembed,view=vc.Myview ,attachments=[file])
                        else:
                            content = f'**{respound.get("queue")}:**\n{fmt}'f'\n{more}' if more else f'**{respound.get("queue")}:**\n{fmt}'
                            vc.np = await vc.interaction.followup.send(content=content, embed=npembed,view=vc.Myview,file=file)
                        return vc.np

class music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.alonetime = bot.config.get('alonetime',0)
        self.nosongtime = bot.config.get('nosongtime',0)
        self.replacer = "$^"
        self.replacement = "."
        self.sptf = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
            )
        )

    # @commands.Cog.listener()
    # async def on_message(self,message:discord.Message):
    #     database = self.bot.mango['music_channel']
    #     data = database.find_one({'guild_id':str(message.guild.id)})
    #     if data:
    #         if message.channel.id == int(data['channel_id']):
    #             await message.delete()
    #             target = await message.channel.fetch_message(data['message_id'])
    #             # if await self.check_ban(message.author.id):
    #             #     respound = get_respound(message.guild.preferred_locale, "baned")
    #             #     embed = createembed.baned(interaction, interaction.client, respound)
    #             #     d = await interaction.followup.send(embed=embed)
    #             #     await asyncio.sleep(5)
    #             #     await d.delete()
    #             #     return
            
    #             # respound = get_respound(interaction.locale, "check_before_play")

    #             if not message.author.voice:
    #                 # embed = createembed.check_before_play(interaction, interaction.client, "usernotin", respound)
    #                 # await interaction.followup.send(embed=embed)
    #                 return
                
    #             elif not message.guild.voice_client:
    #                 vc: wavelink.Player = await message.author.voice.channel.connect(cls=wavelink.Player)

    #             elif message.guild.voice_client.channel != message.author.voice.channel:
    #                 # embed = createembed.check_before_play(interaction, interaction.client, "diffchan", respound)
    #                 # await interaction.followup.send(embed=embed)
    #                 return
                
    #             else:
    #                 vc: wavelink.Player = message.guild.voice_client

    #             await message.guild.change_voice_state(channel=message.author.voice.channel, self_mute=False, self_deaf=True)
    #             search = message.content
    #             await self.statistic(search)

    #             if not vc.playing and not vc.queue:
    #                 setattr(vc, "np", target)
    #                 setattr(vc, "loop", "False")
    #                 setattr(vc, "task", None)
    #                 setattr(vc, "Myview", None)
    #                 setattr(vc, "interaction", message)
    #                 pre = pr(message,nowplaying.np)
    #                 pl = pp(message,nowplaying.np)
    #                 loop = lo(message,nowplaying.np)
    #                 skip = sk(message,nowplaying.np)
    #                 # voldown = dw(interaction)
    #                 # volup = uw(interaction)
    #                 # clear = cl(interaction)
    #                 auto = au(message,nowplaying.np)
    #                 disconnect = dc(message,nowplaying.np)
    #                 vc.Myview = View(timeout=None)
    #                 vc.Myview.add_item(loop)
    #                 vc.Myview.add_item(auto)
    #                 vc.Myview.add_item(pre)
    #                 vc.Myview.add_item(pl)
    #                 vc.Myview.add_item(skip)
    #                 # vc.Myview.add_item(voldown)
    #                 # vc.Myview.add_item(volup)
    #                 # vc.Myview.add_item(clear)
    #                 vc.Myview.add_item(disconnect)

    #             vc.autoplay = wavelink.AutoPlayMode.partial
    #             # -------Lplaylist
    #             if search == "Lplaylist":
    #                 if await self.check_vip(message.author.id):
    #                     database = self.bot.mango["lplaylist"]
    #                     data = database.find_one({"user_id": str(message.author.id)})
    #                     if not data:
    #                         # respound = get_respound(message.guild.preferred_locale, "callback")
    #                         # embed = createembed.playnolplaylist(interaction, self.bot, respound)
    #                         # await interaction.followup.send(embed=embed)
    #                         return

    #                     first = None
    #                     for title, uri in data["playlist"].items():
    #                         source = await createsource.searchen(
    #                             self,
    #                             uri.replace(self.replacer, self.replacement),
    #                             message.author,
    #                         )
    #                         if not first:
    #                             first = source
    #                         if not vc.queue and not vc.playing:
    #                             await vc.queue.put_wait(source)
    #                             await vc.play(await vc.queue.get_wait())
    #                         else:
    #                             await vc.queue.put_wait(source)
    #                             await nowplaying.np3(self, message)
    #                             print(f'adding Lplaylist {source}')
    #                     # await self.addtoqueue(
    #                     #     first, interaction,playlist_title='Lplaylist', playlist=True, number=len(data["playlist"])
    #                     # )
    #                     return
    #                 else:
    #                     respound = get_respound(message.guild.preferred_locale, "callback")
    #                     # embed = createembed.noviplplaylist(interaction, self.bot, respound)
    #                     # await interaction.followup.send(embed=embed)
    #                     return
    #             yt = False
    #             if "onlytube" in search:
    #                 yt = True
    #                 search = search.replace("onlytube", "")
    #             track = await createsource.searchen(self, search, message.author, onlyyt=yt)
    #             if track == None:
    #                 # embed = createembed.noresult(interaction, self.bot, respound)
    #                 # await interaction.followup.send(embed=embed)
    #                 print('track not found')
    #                 return
                
    #             if not vc.playing and not vc.queue:
    #                 await vc.queue.put_wait(track)
    #                 await vc.set_volume(100)
    #                 await vc.play(await vc.queue.get_wait())
    #                 print(f"playing {vc.current} requested by {vc.current.extras.requester}")
    #             else:
    #                 await vc.queue.put_wait(track)
    #                 print(f'adding {track}')
    #                 # await self.addtoqueue(track, interaction)
    #                 await nowplaying.np3(self, message)

    @app_commands.command(
        name="createmusicchannel",
        description="create new music channel for songs",
    )
    async def create_music_channel(self, interaction: discord.Interaction,title:str):
        await interaction.response.defer()
        database = self.bot.mango['music_channel']
        data = database.find_one({'guild_id':str(interaction.guild.id)})
        if data:
            try:
               await interaction.guild.fetch_channel(int(data['channel_id']))
               await interaction.followup.send("มีช่องเพลงอยู่เเล้ว")
               return
            except Exception as e :
               logger.error(e)
               database.delete_one({'guild_id':str(interaction.guild.id)})
        text_channel = await interaction.guild.create_text_channel(name=title,category=interaction.channel.category)
        npembed = discord.Embed(
            title=f"LittLeBirDD Music  <a:blobdancee:969575788389220392>",
            color=0xFFFFFF,
        )
        npembed.add_field(
            name=f"ระยะเวลา", value=f"`0:00:00/0:00:00`"
        )
        npembed.set_footer(
            text=f"Not Playing | 100% | LoopStatus:Disable | Autoplay:Disable"
        )
        # npembed.set_thumbnail(url=vc.current.artwork)
        pre = pr(interaction)
        pl = pp(interaction)
        loop = lo(interaction)
        skip = sk(interaction)
        # voldown = dw(interaction)
        # volup = uw(interaction)
        # clear = cl(interaction)
        auto = au(interaction)
        Myview = View(timeout=None)
        disconnect = dc(interaction)
        Myview.add_item(loop)
        Myview.add_item(auto)
        Myview.add_item(pre)
        Myview.add_item(pl)
        Myview.add_item(skip)
        # vc.Myview.add_item(voldown)
        # vc.Myview.add_item(volup)
        # vc.Myview.add_item(clear)
        Myview.add_item(disconnect)
        with io.BytesIO() as image_binary:
            total = 100
            progress = 0
            w, h =  350, 10
            r=3
            length = (progress*w)/total
            img = Image.new("RGBA", (w, h)) 
            img1 = ImageDraw.Draw(img)   
            img1.line(xy=(-1,5,350,5),fill ="white",width=2) 
            img1.ellipse(xy=(length-r,5-r,length+r,5+r) ,fill='darkred')
            img.save(image_binary,'PNG')
            image_binary.seek(0)

            file = discord.File(image_binary, filename="image.png")

            npembed.set_image(url="attachment://image.png")
            # vc.np = await vc.interaction.followup.send(content=content, embed=npembed,view=vc.Myview,file=file)
         
            np = await text_channel.send(content='ไม่มีเพลงในคิวเเล้ว',embed=npembed,file=file,view=Myview)
            database.insert_one({
            "guild_id":str(interaction.guild.id),
            "channel_id":str(text_channel.id),
            "message_id":str(np.id)
                })
                     
    async def check_ban(self, v):
        if self.bot.mango["ban"].find_one({"user_id": str(v)}):
            return True
        else:
            return False

    async def cleanup(self, guild, frm):
        vc: wavelink.Player = guild.voice_client
        if vc == None:
            return
        vc.queue.clear()
        try:
            await vc.np.delete()
        except:
            pass
        await vc.disconnect()

    async def check_before_play(self, interaction: discord.Interaction):
        vc: wavelink.Player = interaction.guild.voice_client
        respound = get_respound(interaction.locale, "check_before_play")
        if vc == None:
            embed = createembed.embed_fail(interaction,respound['novc'])
            await interaction.followup.send(embed=embed)
            return False
        if interaction.user.voice == None:
            embed = createembed.embed_fail(interaction,respound['usernotin'])
            await interaction.followup.send(embed=embed)
            return False
        if interaction.guild.voice_client.channel != interaction.user.voice.channel:
            embed = createembed.embed_fail(interaction,respound['diffchan'])
            await interaction.followup.send(embed=embed)
            return False
        return True

    @commands.Cog.listener()
    async def on_wavelink_track_exception(self, exp:wavelink.TrackExceptionEventPayload):
        interaction: discord.Interaction = exp.player.interaction
        vc:wavelink.Player = interaction.guild.voice_client
        respound = get_respound(interaction.locale, "on_wavelink_track_exception")
        await asyncio.sleep(2)
        if not vc.paused:
            await vc.stop()
        try:
            await vc.np.delete()
        except:pass
        vc.np = None
        await vc.stop()
        embed = createembed.embed_fail(interaction, respound)
        d = await interaction.followup.send(embed=embed)
        await asyncio.sleep(5)
        await d.delete()

    async def check_vip(self, v):
        if self.bot.mango["vip"].find_one({"user_id": str(v)}):
            return True
        else:
            return False

    @app_commands.command(name="nowplaying", description="Show current music")
    async def nowplaying(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if await self.check_ban(interaction.user.id):
            respound = get_respound(interaction.locale, "baned")
            embed = createembed.embed_fail(interaction, respound)
            d = await interaction.followup.send(embed=embed)
            await asyncio.sleep(5)
            await d.delete()
            return
        if await self.check_before_play(interaction):
            vc: wavelink.Player = interaction.guild.voice_client
            vc.interaction = interaction
            try:
                vc.task.cancel() # To prevent bot from send Nowplaying message twice
            except:
                pass
            vc.task = self.bot.loop.create_task(self.current_time(vc.interaction))

    @app_commands.command(
        name="autoplay",
        description="when ran out of music bot will random music for you",
    )
    async def autoplay(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if await self.check_ban(interaction.user.id):
            respound = get_respound(interaction.locale, "baned")
            embed = createembed.embed_fail(interaction, respound)
            d = await interaction.followup.send(embed=embed)
            await asyncio.sleep(5)
            await d.delete()
            return
        
        
        if await self.check_before_play(interaction):
            vc: wavelink.Player = interaction.guild.voice_client
            vc.interaction = interaction
            if await self.check_vip(interaction.user.id):
                au = [x for x in vc.Myview.children if x.custom_id == "au"][0]
                if vc.autoplay == wavelink.AutoPlayMode.partial:
                    vc.autoplay = wavelink.AutoPlayMode.enabled
                    au.style = discord.ButtonStyle.green
                elif vc.autoplay == wavelink.AutoPlayMode.enabled:
                    vc.autoplay = wavelink.AutoPlayMode.partial
                    au.style = discord.ButtonStyle.gray
                await nowplaying.np(self, interaction)
                respound = get_respound(interaction.locale, "autoplay")
                embed = createembed.embed_success(interaction, respound)
                d = await interaction.followup.send(embed=embed)
                await asyncio.sleep(5)
                await d.delete()
            else:
                respound = get_respound(interaction.locale, "viponly")
                embed = createembed.embed_fail(interaction, respound)
                d = await interaction.followup.send(embed=embed)
                await asyncio.sleep(5)
                await d.delete()

    def is_url(self,url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False
    
    async def statistic(self, search):
        search = search.replace(self.replacement, self.replacer)
        if len(search) > 99:
            return
        
        if self.is_url(search):
            return
        
        database = self.bot.mango["searchstatistic2"]
        data = database.find_one({"music": search})
        if not data:
            database.insert_one({"music": search, "times": 1})
        else:
            database.update_one({"music": search}, {"$inc": {"times": 1}})

    # @app_commands.command(name="play_local", description="Play local audio file")
    # @app_commands.describe(audio="Drop or brows file")
    # async def play_local(
    #     self, interaction: discord.Interaction, audio: discord.Attachment
    # ):
    #     await interaction.response.defer()
    #     if await self.check_ban(interaction.user.id):
    #         respound = get_respound(interaction.locale, "baned")
    #         embed = createembed.baned(interaction, interaction.client, respound)
    #         d = await interaction.followup.send(embed=embed)
    #         await asyncio.sleep(5)
    #         await d.delete()
    #         return
    #     respound = get_respound(interaction.locale, "check_before_play")
    #     if not interaction.user.voice:
    #         embed = createembed.check_before_play(
    #             interaction, interaction.client, "usernotin", respound
    #         )
    #         await interaction.followup.send(embed=embed)
    #         return
    #     elif not interaction.guild.voice_client:
    #         vc: wavelink.Player = await interaction.user.voice.channel.connect(
    #             cls=wavelink.Player
    #         )
    #     elif interaction.guild.voice_client.channel != interaction.user.voice.channel:
    #         embed = createembed.check_before_play(
    #             interaction, interaction.client, "diffchan", respound
    #         )
    #         await interaction.followup.send(embed=embed)
    #         return
    #     else:
    #         vc: wavelink.Player = interaction.guild.voice_client
    #     await interaction.guild.change_voice_state(
    #         channel=interaction.user.voice.channel, self_mute=False, self_deaf=True
    #     )
    #     if not vc.is_playing() and vc.queue.is_empty:
    #         setattr(vc, "loading", None)
    #         setattr(vc, "np", None)
    #         setattr(vc, "loop", "False")
    #         setattr(vc, "task", None)
    #         setattr(vc, "nosong", None)
    #         setattr(vc, "Myview", None)
    #         setattr(vc, "autoplay", False)
    #         setattr(vc, "interaction", interaction)
    #         setattr(vc, "history_autoplay_track", [])
    #         setattr(vc, "state", "normal")
    #         pl = pp(interaction)
    #         loop = lo(interaction)
    #         skip = sk(interaction)
    #         voldown = dw(interaction)
    #         volup = uw(interaction)
    #         clear = cl(interaction)
    #         auto = au(interaction)
    #         disconnect = dc(interaction)
    #         vc.Myview = View(timeout=None)
    #         vc.Myview.add_item(loop)
    #         vc.Myview.add_item(auto)
    #         vc.Myview.add_item(pl)
    #         vc.Myview.add_item(skip)
    #         vc.Myview.add_item(voldown)
    #         vc.Myview.add_item(volup)
    #         vc.Myview.add_item(clear)
    #         vc.Myview.add_item(disconnect)
    #     vc.interaction = interaction
    #     basename = "audio"
    #     suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    #     filename = "_".join([basename, suffix])
    #     path = f"{os.getcwd()}\cf\\{filename}.wav"
    #     await audio.save(path)
    #     result = await wavelink.LocalTrack.search(path, return_first=True)
    #     result.title = audio.filename
    #     track = {
    #         "song": result,
    #         "requester": interaction.user,
    #         "source": "Local track",
    #         "path": path,
    #     }
    #     if not vc.is_playing() and vc.queue.is_empty:
    #         await vc.queue.put_wait(track)
    #         await vc.set_volume(100)
    #         await vc.play(vc.queue[0]["song"], populate=True)
    #     else:
    #         await vc.queue.put_wait(track)
    #         await self.addtoqueue(track, interaction)

    @app_commands.command(name="play", description="play music")
    @app_commands.describe(search="Music name")
    async def play(self, interaction: discord.Interaction, search: str):
        await interaction.response.defer()

        if await self.check_ban(interaction.user.id):
            respound = get_respound(interaction.locale, "baned")
            embed = createembed.embed_fail(interaction, respound)
            d = await interaction.followup.send(embed=embed)
            await asyncio.sleep(5)
            await d.delete()
            return
        
        respound = get_respound(interaction.locale, "check_before_play")
        if not interaction.user.voice:
            embed = createembed.embed_fail(interaction,respound['usernotin'])
            await interaction.followup.send(embed=embed)
            return
        
        elif not interaction.guild.voice_client:
            vc: wavelink.Player = await interaction.user.voice.channel.connect(cls=wavelink.Player)

        elif interaction.guild.voice_client.channel != interaction.user.voice.channel:
            embed = createembed.embed_fail(interaction,respound['diffchan'])
            await interaction.followup.send(embed=embed)
            return
        
        else:
            vc: wavelink.Player = interaction.guild.voice_client

        await interaction.guild.change_voice_state(channel=interaction.user.voice.channel, self_mute=False, self_deaf=True)

        await self.statistic(search)

        if not vc.playing and not vc.queue:
            setattr(vc, "np", None)
            setattr(vc, "loop", "False")
            setattr(vc, "task", None)
            setattr(vc, "Myview", None)
            setattr(vc, "interaction", interaction)
            pre = pr(interaction,nowplaying.np)
            pl = pp(interaction,nowplaying.np)
            loop = lo(interaction,nowplaying.np)
            skip = sk(interaction,nowplaying.np)
            # voldown = dw(interaction)
            # volup = uw(interaction)
            # clear = cl(interaction)
            auto = au(interaction,nowplaying.np)
            disconnect = dc(interaction,nowplaying.np)
            vc.Myview = View(timeout=None)
            vc.Myview.add_item(loop)
            vc.Myview.add_item(auto)
            vc.Myview.add_item(pre)
            vc.Myview.add_item(pl)
            vc.Myview.add_item(skip)
            # vc.Myview.add_item(voldown)
            # vc.Myview.add_item(volup)
            # vc.Myview.add_item(clear)
            vc.Myview.add_item(disconnect)
            vc.autoplay = wavelink.AutoPlayMode.partial

        vc.interaction = interaction
        # -------Lplaylist
        if search == "Lplaylist":
            if await self.check_vip(interaction.user.id):
                database = self.bot.mango["lplaylist"]
                data = database.find_one({"user_id": str(interaction.user.id)})
                if not data:
                    respound = get_respound(interaction.locale, "playnolplaylist")
                    embed = createembed.embed_fail(interaction, respound)
                    await interaction.followup.send(embed=embed)
                    return
                first = None
                for title, uri in data["playlist"].items():
                    source = await createsource.searchen(
                        self,
                        uri.replace(self.replacer, self.replacement),
                        interaction.user,
                    )
                    if not first:
                        first = source
                    if not vc.queue and not vc.playing:
                        await vc.queue.put_wait(source)
                        await vc.play(await vc.queue.get_wait())
                    else:
                        await vc.queue.put_wait(source)
                        await nowplaying.np(self, interaction)
                        logger.info(f'adding Lplaylist {source}')
                await self.addtoqueue(
                    first, interaction,playlist_title='Lplaylist', playlist=True, number=len(data["playlist"])
                )
                return
            else:
                respound = get_respound(interaction.locale, "viponly")
                embed = createembed.embed_fail(interaction, respound)
                await interaction.followup.send(embed=embed)
                return
        yt = False
        if "onlytube" in search:
            yt = True
            search = search.replace("onlytube", "")
        track = await createsource.searchen(self, search, interaction.user, onlyyt=yt)
        if track == None:
            respound = get_respound(interaction.locale, "noresult")
            embed = createembed.embed_fail(interaction, respound)
            await interaction.followup.send(embed=embed)
            return
        
        if not vc.playing and not vc.queue:
            await vc.queue.put_wait(track)
            await vc.set_volume(100)
            await vc.play(await vc.queue.get_wait(),populate=True)
            logger.info(f"playing {vc.current} requested by {vc.current.extras.requester}")
        else:
            await vc.queue.put_wait(track)
            logger.info(f'adding {track}')
            await self.addtoqueue(track, interaction)
            await nowplaying.np(self, interaction)

    # @play.autocomplete('search')
    # async def fruits_autocomplete(self,interaction: discord.Interaction,current: str,) -> List[app_commands.Choice[str]]:
    #     if len(current) == 0:
    #       alphabet = "abcdefghijklmnopqrstuvwxyzกขคตงจฉชซณญพรสวงฬฒฮผอป"
    #       current = random.choice(alphabet)
    #     result = await wavelink.YouTubeMusicTrack.search(current)
    #     return [app_commands.Choice(name=l.title, value=current)for l in result if current.lower() in l.title.lower()]

    @play.autocomplete("search")
    async def fruits_autocomplete(
        self,
        interaction,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        database = self.bot.mango["searchstatistic2"]
        source = database.find().sort("times", -1).limit(3)
        if len(current) > 0:
            source = database.find({"music": {"$regex": current,'$options' : 'i'}}).limit(25)
        return [app_commands.Choice(name=l["music"].replace(self.replacer, self.replacement),value=l["music"].replace(self.replacer, self.replacement))for l in source]

    def convert(self, seconds):
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        return "%d:%02d:%02d" % (hour, minutes, seconds)

    async def addtoqueue(self, track:wavelink.Playable|wavelink.Playlist, interaction, playlist=False, number=None,playlist_title=None):
        respound = get_respound(interaction.locale, "addtoqueue")
        if isinstance(track,wavelink.Playlist):
            number = len(track.tracks)
            playlist_title = track.name
            track = track.tracks[0]
            playlist = True
            
        if not playlist:
            embed = discord.Embed(
                title=track.title,
                description=f"{respound.get('added')} ✅",
                color=0x19AD3B,
            )
            embed.set_footer(
                text=f"{respound.get('addedby').format(user=interaction.user.name)}",
                icon_url=interaction.user.avatar.url,
            )
            embed.set_thumbnail(url=track.artwork)
            d = await interaction.followup.send(embed=embed)
            await asyncio.sleep(5)
            await d.delete()
        else:
            embed = discord.Embed(
                title=respound.get("addplaylist").format(title=playlist_title,number=number),
                description=f"{respound.get('added')} ✅",
                color=0x19AD3B,
            )
            embed.set_footer(
                text=f"{respound.get('addedby').format(user=interaction.user.name)}",
                icon_url=interaction.user.avatar.url,
            )
            embed.set_thumbnail(url=track.artwork)
            d = await interaction.followup.send(embed=embed)
            await asyncio.sleep(5)
            await d.delete()

    async def current_time(self, interaction):
        vc: wavelink.Player = interaction.guild.voice_client
        try:
            await vc.np.delete()
        except:pass
        vc.np = None
        while True:
            vc: wavelink.Player = interaction.guild.voice_client
            if interaction.is_expired():
                try:
                    vc.task.cancel()
                except:pass
            elif not interaction.is_expired() and vc.task.cancelled(): # resume update nowplaying after get new interaction
                vc.task = self.bot.loop.create_task(self.current_time(vc.interaction))
            try:
                np = await nowplaying.np(self,interaction)
            except discord.errors.NotFound as e:
                break
            if vc == None:
                break
            if vc.np == None:
                break
            await asyncio.sleep(9)
            await asyncio.sleep(1)
        vc.task.cancel()

    # --------------------------------

    async def corrected_song_name(self, title: str) -> str:
        st = self.bot.last.search_for_track("", title)
        searchtrack = st.get_next_page()
        if searchtrack:
            track = searchtrack[0]
            result = f"{track.title} - {track.artist} "
            logger.info(f"last.fm | {title} -> {result}")
        else:
            corrected_title = self.sptf.search(q=title, type="track", limit=1)[
                "tracks"
            ]["items"]
            if corrected_title:
                track = corrected_title[0]
                result = f"{track['name']} - {track['artists'][0]['name']}"
                logger.info(f"spotify | {title} -> {result}")
            else:
                result = None
        return result

    @commands.Cog.listener()
    async def on_wavelink_track_start(self, payload:wavelink.payloads.TrackStartEventPayload):
        vc: wavelink.Player = payload.player
        if not vc:
            return
        if not dict(vc.current.extras).get('requester',None):
            vc.current.extras = {'requester': 'Recommended','requester_icon' : payload.player.client.user.avatar.url}
        logger.info(f"Now playing : {vc.current}")
        await asyncio.sleep(0.3)
        vc.task = self.bot.loop.create_task(self.current_time(vc.interaction))

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload:wavelink.payloads.TrackEndEventPayload):
        logger.info(f"ending: {payload.track}")
        vc: wavelink.Player = payload.player
        if not vc:
            return
        vc.task.cancel()
        try:
            await vc.np.delete()
        except:
            pass
        vc.np = None
        if payload.player == None:
            return
        interaction = payload.player.interaction
        respound = get_respound(interaction.locale, "on_wavelink_track_end")
        if not vc.queue and vc:
            try:
                async with timeout(self.nosongtime):
                    await self.nosong(interaction)
            except:
                await self.cleanup(interaction.guild, "trackend")
                embed = createembed.embed_info(vc.interaction, respound)
                try:
                    d = await interaction.followup.send(embed=embed)
                    await asyncio.sleep(5)
                    await d.delete()
                except:
                    pass
                return
        # if vc == None:
        #     return
        # if vc.state == "disconnect":
        #     return
        # respound = get_respound(interaction.locale, "on_wavelink_track_end")
        # try:
        #     if vc.queue[0].get("path", None) != None:
        #         os.remove(vc.queue[0]["path"])
        # except:
        #     pass
        # if vc:
        #     try:
        #         recent_song = vc.queue[0]
        #     except:
        #         recent_song = None
        #     vc.task.cancel()
        #     await asyncio.sleep(0.2)
        #     try:
        #         await vc.np.delete()
        #     except:
        #         pass
        #     vc.np = None
        #     if not vc.queue.is_empty:
        #         if vc.loop == "False":
        #             del vc.queue[0]
        #         elif vc.loop == "Song":
        #             pass
        #         elif vc.loop == "Queue":
        #             get = vc.queue[0]
        #             del vc.queue[0]
        #             await vc.queue.put_wait(get)

        #     if vc.queue.is_empty:
        #         if vc.autoplay:
        #             next_auto = None
        #             search = recent_song["song"].title
        #             if recent_song["artist"]:
        #                 search = f"{search} - {recent_song['artist']}"
        #             corrected_name = await self.corrected_song_name(search)
        #             tracks = None
        #             if corrected_name:
        #                 searchtrack = self.bot.last.search_for_track(
        #                     "", corrected_name
        #                 ).get_next_page()
        #                 if searchtrack:
        #                     tracks = searchtrack[0]
        #                     similar = tracks.get_similar(limit=15)
        #                     if similar:
        #                         rand = random.choice(similar).item
        #                         engine = "last.fm"
        #                         next_auto = f"{rand.title} - {rand.artist.name}"
        #                         next_artist = rand.artist.name

        #             if next_auto == None and tracks != None:
        #                 searchart = self.bot.last.get_artist(tracks.artist)
        #                 similar: list = searchart.get_top_tracks(limit=7)
        #                 times = 0
        #                 while times <= 50:
        #                     if not similar:
        #                         break
        #                     rand = random.choice(similar)
        #                     if rand.item != tracks:
        #                         if (
        #                             f"{rand.item.title} - {rand.item.artist}"
        #                             not in vc.history_autoplay_track
        #                         ):
        #                             next_auto = (
        #                                 f"{rand.item.title} - {rand.item.artist.name}"
        #                             )
        #                             next_artist = rand.item.artist.name
        #                             engine = "last.fm (artist)"
        #                             vc.history_autoplay_track.append(next_auto)
        #                             break
        #                     times += 1

        #             if next_auto == None:
        #                 results = self.sptf.search(
        #                     q=corrected_name, type="track", limit=10
        #                 )
        #                 if results["tracks"]["total"] != 0:
        #                     track = results["tracks"]["items"][0]
        #                     track_url = results["tracks"]["items"][0]["external_urls"][
        #                         "spotify"
        #                     ]
        #                     artist_url = results["tracks"]["items"][0]["artists"][0][
        #                         "external_urls"
        #                     ]["spotify"]
        #                     similar_tracks = self.sptf.recommendations(
        #                         seed_tracks=[track_url],
        #                         seed_artists=[artist_url],
        #                         limit=10,
        #                     )
        #                     # for i, track in enumerate(similar_tracks['tracks'], start=1):
        #                     #   print(f"{i}. {track['name']} - {track['artists'][0]['name']} {track['external_urls']['spotify']}")
        #                     if similar_tracks:
        #                         rand = random.choice(similar_tracks["tracks"])
        #                         engine = "spotify recommendations"
        #                         next_artist = rand["artists"][0]["name"]
        #                         next_auto = f"{rand['name']} - {next_artist}"

        #             if next_auto == None:
        #                 lang = [None, "Thai"]
        #                 l = random.choice(lang)
        #                 random_song = None
        #                 while random_song is None:
        #                     try:
        #                         random_song = get_random(
        #                             spotify=self.bot.spotify_client,
        #                             year="2020-2022",
        #                             limit=20,
        #                             offset_max=50,
        #                             type="track",
        #                             genre=l,
        #                         )
        #                     except:
        #                         pass
        #                 engine = "Random alphabet"
        #                 next_auto = random_song["external_urls"]["spotify"]
        #                 next_artist = random_song["artists"][0]["name"]

        #             print(f"next music : {next_auto} ({engine})")
        #             print("---------------------------------------------")
        #             track = await createsource.searchen(
        #                 self, next_auto, self.bot, next_artist
        #             )
        #             await vc.queue.put_wait(track)
        #     if not vc.queue.is_empty:
        #         await vc.play(vc.queue[0]["song"])
        #         await nowplaying.np(self, vc.interaction)
        #         vc.task = self.bot.loop.create_task(self.current_time(interaction))
        #     if vc.queue.is_empty:
        #         try:
        #             async with timeout(self.nosongtime):
        #                 await self.nosong(interaction)
        #         except:
        #             await self.cleanup(interaction.guild, "trackend")
        #             embed = createembed.on_wavelink_track_end(
        #                 vc.interaction, self.bot, respound
        #             )
        #             try:
        #                 d = await interaction.followup.send(embed=embed)
        #                 await asyncio.sleep(5)
        #                 await d.delete()
        #             except:
        #                 pass
        #             return

    async def nosong(self, interaction:discord.Interaction):
        i=0
        while True:
            vc: wavelink.Player = interaction.guild.voice_client
            if vc.queue or vc.current:
                break
            i+=1
            logger.info(f'counting no song {interaction.guild.name} | {i}')
            await asyncio.sleep(0.4)

    @app_commands.command(name="loop", description="Set music loop status")
    @app_commands.describe(status="loop status")
    @app_commands.choices(
        status=[
            Choice(name="False (ปิด)", value='wavelink.QueueMode.normal'),
            Choice(name="Song (เพลง)", value="wavelink.QueueMode.loop"),
            Choice(name="Queue (ทั้งคิว)", value="wavelink.QueueMode.loop_all"),
        ]
    )
    async def loop(self, interaction: discord.Interaction, status: str):
        await interaction.response.defer()
        if await self.check_ban(interaction.user.id):
            respound = get_respound(interaction.locale, "baned")
            embed = createembed.embed_fail(interaction, respound)
            d = await interaction.followup.send(embed=embed)
            await asyncio.sleep(5)
            await d.delete()
            return
        if await self.check_before_play(interaction):
            vc: wavelink.Player = interaction.guild.voice_client
            vc.interaction = interaction
            vc.queue.mode = eval(status)
            lo = [x for x in vc.Myview.children if x.custom_id == "lo"][0]
            if vc.queue.mode == wavelink.QueueMode.normal:
                lo.style = discord.ButtonStyle.gray
            elif vc.queue.mode == wavelink.QueueMode.loop:
                lo.style = discord.ButtonStyle.blurple
            elif vc.queue.mode == wavelink.QueueMode.loop_all:
                lo.style = discord.ButtonStyle.green
            await nowplaying.np(self, interaction)
            respound = get_respound(interaction.locale, "loop")
            embed = createembed.embed_success(interaction, respound,trans_queueMode[status])
            d = await interaction.followup.send(embed=embed)
            await asyncio.sleep(5)
            await d.delete()

    @app_commands.command(name="resume", description="Resume music")
    async def resume(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if await self.check_ban(interaction.user.id):
            respound = get_respound(interaction.locale, "baned")
            embed = createembed.embed_fail(interaction, respound)
            d = await interaction.followup.send(embed=embed)
            await asyncio.sleep(5)
            await d.delete()
            return
        if await self.check_before_play(interaction):
            vc: wavelink.Player = interaction.guild.voice_client
            vc.interaction = interaction
            re = [x for x in vc.Myview.children if x.custom_id == "pp"][0]
            re.style = discord.ButtonStyle.green
            re.emoji = "<a:1_:989120454063185940>"
            await vc.pause(False)
            respound = get_respound(interaction.locale, "resume")
            embed = createembed.embed_success(interaction, respound)
            d = await interaction.followup.send(embed=embed)
            await asyncio.sleep(5)
            await d.delete()

    @app_commands.command(name="pause", description="Pause music")
    async def pause(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if await self.check_ban(interaction.user.id):
            respound = get_respound(interaction.locale, "baned")
            embed = createembed.embed_fail(interaction, respound)
            d = await interaction.followup.send(embed=embed)
            await asyncio.sleep(5)
            await d.delete()
            return
        respound = get_respound(interaction.locale, "pause")
        if await self.check_before_play(interaction):
            vc: wavelink.Player = interaction.guild.voice_client
            vc.interaction = interaction
            re = [x for x in vc.Myview.children if x.custom_id == "pp"][0]
            re.style = discord.ButtonStyle.red
            re.emoji = "<a:2_:989120456240025670>"
            await vc.pause(True)
            await nowplaying.np(self, interaction)
            respound = get_respound(interaction.locale, "pause")
            embed = createembed.embed_success(interaction, respound)
            d = await interaction.followup.send(embed=embed)
            await asyncio.sleep(5)
            await d.delete()

    @app_commands.command(name="skip", description="Skip music")
    @app_commands.describe(to="Skip to given music")
    async def skip(self, interaction: discord.Interaction, to: Optional[int] = False):
        await interaction.response.defer()
        if await self.check_ban(interaction.user.id):
            respound = get_respound(interaction.locale, "baned")
            embed = createembed.embed_fail(interaction, respound)
            d = await interaction.followup.send(embed=embed)
            await asyncio.sleep(5)
            await d.delete()
            return
        if await self.check_before_play(interaction):
            vc: wavelink.Player = interaction.guild.voice_client
            vc.interaction = interaction
            if to:
                respound = get_respound(interaction.locale, "skipto")
                if to > len(vc.queue):
                    embed = createembed.embed_fail(interaction, respound)
                    await interaction.followup.send(embed=embed)
                    return
                wanted = vc.queue[to-1]
                vc.queue.delete(to-1)
                vc.queue.put_at(0,wanted)
                await vc.skip()
                embed = createembed.embed_success(interaction, respound,to)
                d = await interaction.followup.send(embed=embed)
                await asyncio.sleep(5)
                await d.delete()
            else:
                await vc.skip()
                respound = get_respound(interaction.locale, "skip")
                embed = createembed.embed_success(interaction, respound)
                d = await interaction.followup.send(embed=embed)
                await asyncio.sleep(5)
                await d.delete()

    @app_commands.command(name="shuffle", description="Shuffle music queue")
    async def shuffle(self, interaction: discord.Interaction):
        await interaction.response.defer()
        vc: wavelink.Player = interaction.guild.voice_client
        if await self.check_ban(interaction.user.id):
            respound = get_respound(interaction.locale, "baned")
            embed = createembed.embed_success(interaction, respound)
            d = await interaction.followup.send(embed=embed)
            await asyncio.sleep(5)
            await d.delete()
            return
        if await self.check_before_play(interaction):
            vc: wavelink.Player = interaction.guild.voice_client
            vc.interaction = interaction
            vc.queue.shuffle()
            respound = get_respound(interaction.locale, "shuffle")
            embed = createembed.embed_success(interaction, respound)
            d = await interaction.followup.send(embed=embed)
            await asyncio.sleep(5)
            await d.delete()

    @app_commands.command(name="disconnect", description="Leave voice chat")
    async def dc(self, interaction: discord.Interaction):
        vc: wavelink.Player = interaction.guild.voice_client
        vc.interaction = interaction
        await interaction.response.defer()
        if await self.check_ban(interaction.user.id):
            respound = get_respound(interaction.locale, "baned")
            embed = createembed.embed_fail(interaction, respound)
            d = await interaction.followup.send(embed=embed)
            await asyncio.sleep(5)
            await d.delete()
            return
        if await self.check_before_play(interaction):
            vc: wavelink.Player = interaction.guild.voice_client
            vc.interaction = interaction
            await self.cleanup(interaction.guild, "dc")
            respound = get_respound(interaction.locale, "dc")
            embed = createembed.embed_success(interaction, respound)
            d = await interaction.followup.send(embed=embed)
            await asyncio.sleep(5)
            await d.delete()

    @app_commands.command(name="remove", description="Remove given music from queue")
    @app_commands.describe(index="Music Sequence")
    async def remove(self, interaction: discord.Interaction, index: int):
        await interaction.response.defer()
        if await self.check_ban(interaction.user.id):
            respound = get_respound(interaction.locale, "baned")
            embed = createembed.embed_fail(interaction, respound)
            d = await interaction.followup.send(embed=embed)
            await asyncio.sleep(5)
            await d.delete()
            return
        if await self.check_before_play(interaction):
            vc: wavelink.Player = interaction.guild.voice_client
            vc.interaction = interaction
            delete = None
            if vc.queue.mode == wavelink.QueueMode.loop_all:
                if index > (vc.queue.count+vc.queue.history.count):#Index out of range handler
                    respound = get_respound(interaction.locale, "remove")
                    erembed = createembed.embed_fail(interaction, respound)
                    await interaction.followup.send(embed=erembed)
                    return
                if index > vc.queue.count: 
                    delete = vc.queue.history.peek(index-len(vc.queue)-1)
                    vc.queue.history.delete(index-len(vc.queue)-1)
                else:
                    delete = vc.queue.peek(index-1)
                    vc.queue.delete(index-1)
            else:
                if index > vc.queue.count: #Index out of range handler
                    respound = get_respound(interaction.locale, "remove")
                    erembed = createembed.embed_fail(interaction, respound)
                    await interaction.followup.send(embed=erembed)
                    return
                delete = vc.queue.peek(index-1)
                vc.queue.delete(index-1)
            respound = get_respound(interaction.locale, "remove")
            embed = createembed.embed_success(interaction, respound,delete)
            d = await interaction.followup.send(embed=embed)
            await asyncio.sleep(5)
            await d.delete()
            await nowplaying.np(self, interaction)

    @remove.error
    async def remove_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.CommandInvokeError):
            await interaction.response.defer()
            respound = get_respound(interaction.locale, "remove")
            erembed = createembed.embed_fail(interaction, respound)
            await interaction.followup.send(embed=erembed)

    @app_commands.command(name="queue", description="Send queuelist")
    async def queueList(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if await self.check_ban(interaction.user.id):
            respound = get_respound(interaction.locale, "baned")
            embed = createembed.embed_fail(interaction, respound)
            d = await interaction.followup.send(embed=embed)
            await asyncio.sleep(5)
            await d.delete()
            return
        if await self.check_before_play(interaction):
            pag = []
            respound = get_respound(interaction.locale, "queueList")
            vc: wavelink.Player = interaction.guild.voice_client
            vc.interaction = interaction
            upcoming = vc.queue
            if vc.queue.mode == wavelink.QueueMode.loop_all:
                upcoming = list(upcoming)+list(vc.queue.history)
            number = len(upcoming)
            page = math.ceil(number / 10)
            if page == 0:
                page = 1
            lst = []

            for index,track in enumerate(upcoming,1):
                op = f'{index}.{track}'
                lst.append(op)

            for i in range(page):
                items = list(itertools.islice(lst, 0, 10))
                if i != 0:
                    fmt = "\n".join(f"**` {_}`**" for _ in items)
                    embed = discord.Embed(color=0xFFFFFF)
                else:
                    fmt = "\n".join(f"**` {_}`**" for _ in items)
                    plus = 1
                    if len(fmt) == 0:
                        plus = 0
                    embed = discord.Embed(
                        title=respound.get("more").format(more=number - plus),
                        color=0xFFFFFF,
                    )
                    if vc.current == None:
                        embed.add_field(
                            name=respound.get("playing"),
                            value=respound.get("noplay"),
                            inline=False,
                        )
                    else:
                        embed.add_field(
                            name=respound.get("playing"),
                            value=f"**`{vc.current.title}`**",
                            inline=False,
                        )
                if number <= 1:
                    embed.add_field(
                        name=respound.get("inqueue"),
                        value=respound.get("nomorequeue"),
                        inline=False,
                    )
                else:
                    embed.add_field(
                        name=respound.get("inqueue"), value=f"{fmt}", inline=False
                    )
                pag.append(embed)
                for i in range(10):
                    try:
                        del lst[0]
                    except:
                        pass
            embed.set_footer(text=respound.get("notupdate"))
            view = buttin(pag, 120, interaction)
            view.interaction = interaction
            await interaction.followup.send(embed=pag[0], view=view)

    async def checkdc(self, member:discord.Member):
        vc: wavelink.Player = member.guild.voice_client
        i=0
        while True:
            i += 1
            logger.info(f'counting alonetime {member.guild.name} | {i}')
            if len(vc.channel.members) > 1:
                break
            await asyncio.sleep(0.5)

    # @app_commands.command(name="filters", description="Modify music with filters")
    # @app_commands.choices(
    #     type=[
    #         Choice(name="Bassboost (เร่งเบส)", value="Bassboost"),
    #         Choice(name="Piano", value="Piano"),
    #         Choice(name="8D ", value="Rotation"),
    #         Choice(name="Speed up (เพิ่มความเร็ว)", value="Increasespeed"),
    #         Choice(name="Speed Down (ลดความเร็ว)", value="Decreasespeed"),
    #         Choice(name="Reset (รีเซ็ต)", value="Reset"),
    #     ]
    # )
    # async def filters(self, interaction: discord.Interaction, type: str):
    #     await interaction.response.defer()
    #     if await self.check_ban(interaction.user.id):
    #         respound = get_respound(interaction.locale, "baned")
    #         embed = createembed.baned(interaction, interaction.client, respound)
    #         d = await interaction.followup.send(embed=embed)
    #         await asyncio.sleep(5)
    #         await d.delete()
    #         return
    #     if await self.check_before_play(interaction):
    #         respound = get_respound(interaction.locale, "filters")
    #         vc: wavelink.Player = interaction.guild.voice_client
    #         if type == "Bassboost":
    #             fil = wavelink.Filters()
    #             fil.
    #             await vc.set_filters(
                    
    #             )
    #         if type == "Piano":
    #             await vc.set_filter(
    #                 wavelink.Filter(equalizer=wavelink.Equalizer.piano())
    #             )
    #         if type == "Increasespeed":
    #             await vc.set_filter(
    #                 wavelink.Filter(timescale=wavelink.Timescale(speed=1.10))
    #             )
    #         if type == "Decreasespeed":
    #             await vc.set_filter(
    #                 wavelink.Filter(timescale=wavelink.Timescale(speed=0.90))
    #             )
    #         if type == "Rotation":
    #             await vc.set_filter(wavelink.Filter(rotation=wavelink.Rotation(0.12)))
    #         if type == "Reset":
    #             await vc.set_filter(
    #                 wavelink.Filter(equalizer=wavelink.Equalizer.flat())
    #             )
    #         embed = createembed.filters(interaction, self.bot, respound, type=type)
    #         d = await interaction.followup.send(embed=embed)
    #         await asyncio.sleep(5)
    #         await d.delete()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before, after):
        vc: wavelink.Player = member.guild.voice_client
        if member == self.bot.user:
            return
        if not vc:
            return
        if before.channel != after.channel:
            if after.channel == vc.channel:
                return
            if after.channel != vc.channel:
                if len(vc.channel.members) <= 1:
                    lastone = member
                    try:
                        async with timeout(self.alonetime):
                            await self.checkdc(member)
                            pass
                    except asyncio.TimeoutError:
                        await self.cleanup(member.guild, "voiceupdate no one")
                        respound = get_respound(lastone.guild.preferred_locale, "ononeleft")
                        embed = createembed.embed_info(lastone, respound)
                        try:
                            d = await vc.interaction.followup.send(embed=embed)
                            await asyncio.sleep(5)
                            await d.delete()
                        except:
                            pass
                        return
                    return


async def setup(bot):
    await bot.add_cog(music(bot))
