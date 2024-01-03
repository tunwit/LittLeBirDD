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
import requests
import random
import os
import datetime
from request_data import request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import datetime
from urllib.parse import urlparse

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
        embed = createembed.check_before_play(
            interaction, interaction.client, "novc", respound
        )
        await interaction.followup.send(embed=embed, ephemeral=True)
        return False
    if interaction.user.voice == None:
        embed = createembed.check_before_play(
            interaction, interaction.client, "usernotin", respound
        )
        await interaction.followup.send(embed=embed, ephemeral=True)
        return False
    if interaction.guild.voice_client.channel != interaction.user.voice.channel:
        embed = createembed.check_before_play(
            interaction, interaction.client, "diffchan", respound
        )
        await interaction.followup.send(embed=embed, ephemeral=True)
        return False
    return True


class pp(Button):
    def __init__(self, interaction):
        super().__init__(
            emoji="<a:1_:989120454063185940>",
            style=discord.ButtonStyle.green,
            custom_id="pp",
        )
        self.interaction = interaction

    async def callback(self, interaction):
        await interaction.response.defer()
        vc: wavelink.Player = interaction.guild.voice_client
        vc.interaction = interaction
        if not await check_before_play(interaction):
            return
        if not vc.paused:
            await vc.pause(True)
        elif vc.paused:
            await vc.pause(False)
        pp = [x for x in vc.Myview.children if x.custom_id == "pp"][0]
        if vc.paused:
            pp.emoji = "<a:2_:989120456240025670>"
            pp.style = discord.ButtonStyle.red
        elif not vc.paused:
            pp.emoji = "<a:1_:989120454063185940>"
            pp.style = discord.ButtonStyle.green
        else:
            pp.emoji = "<a:1_:989120454063185940>"
            pp.style = discord.ButtonStyle.green
        await nowplaying.np(self, self.interaction)
        try:
            await interaction.followup.send(content="")
        except:
            pass

class pr(Button):
    def __init__(self, interaction):
        super().__init__(
            emoji="<a:10:989120441325068308>", style=discord.ButtonStyle.blurple
        )
        self.interaction = interaction

    async def callback(self, interaction):
        await interaction.response.defer()
        vc: wavelink.Player = interaction.guild.voice_client
        vc.interaction = interaction
        if not await check_before_play(interaction):
            return
        respound = get_respound(interaction.locale, "previous")
        if len(vc.queue.history) < 2:
            await interaction.followup.send(content=respound.get('noprevious'),ephemeral=True)
            return
        pre_queuemode =  vc.queue.mode
        vc.queue.mode = wavelink.QueueMode.normal

        
        vc.queue._queue.insert(0,vc.queue.history[-1]) #insert current song
        await vc.queue.history.delete(len(vc.queue.history)-1)#delete the current song
        vc.queue._queue.insert(0,vc.queue.history[-1]) #insert previous song       
        await vc.queue.history.delete(len(vc.queue.history)-1) #delete the previous song
        await vc.skip() #play previous song

        vc.queue.mode = pre_queuemode
        try:
            await interaction.followup.send(content="")
        except:
            pass


class sk(Button):
    def __init__(self, interaction):
        super().__init__(
            emoji="<a:10:989120439655739432>", style=discord.ButtonStyle.blurple
        )
        self.interaction = interaction

    async def callback(self, interaction):
        await interaction.response.defer()
        vc: wavelink.Player = interaction.guild.voice_client
        vc.interaction = interaction
        if not await check_before_play(interaction):
            return
        await vc.skip()
        try:
            await interaction.followup.send(content="")
        except:
            pass


class lo(Button):
    def __init__(self, interaction):
        super().__init__(
            emoji="<a:4_:989120448312803348>",
            style=discord.ButtonStyle.gray,
            custom_id="lo",
        )
        self.interaction = interaction

    async def callback(self, interaction):
        await interaction.response.defer()
        vc: wavelink.Player = interaction.guild.voice_client
        vc.interaction = interaction
        lo = [x for x in vc.Myview.children if x.custom_id == "lo"][0]
        if not await check_before_play(self.interaction):
            return
        if vc.queue.mode == wavelink.QueueMode.normal:
            vc.queue.mode = wavelink.QueueMode.loop
            lo.style = discord.ButtonStyle.blurple
        elif vc.queue.mode == wavelink.QueueMode.loop:
            vc.queue.mode = wavelink.QueueMode.loop_all
            lo.style = discord.ButtonStyle.green
        elif vc.queue.mode == wavelink.QueueMode.loop_all:
            vc.queue.mode = wavelink.QueueMode.normal
            lo.style = discord.ButtonStyle.gray
        await nowplaying.np(self, interaction)
        try:
            await interaction.followup.send(content="")
        except:
            pass


class dw(Button):
    def __init__(self, interaction):
        super().__init__(
            emoji="<a:6_:989120452075094026>", style=discord.ButtonStyle.blurple
        )
        self.interaction = interaction

    async def callback(self, interaction):
        await interaction.response.defer()
        vc: wavelink.Player = interaction.guild.voice_client
        vc.interaction = interaction
        if not await check_before_play(interaction):
            return
        if vc.volume - 15 < 0:
            volume = 0
        else:
            volume = vc.volume - 15
        await vc.set_volume(volume)
        await nowplaying.np(self, self.interaction)
        try:
            await interaction.followup.send(content="")
        except:
            pass


class uw(Button):
    def __init__(self, interaction):
        super().__init__(
            emoji="<a:5_:989120450254737418>", style=discord.ButtonStyle.blurple
        )
        self.interaction = interaction

    async def callback(self, interaction):
        await interaction.response.defer()
        vc: wavelink.Player = interaction.guild.voice_client
        vc.interaction = interaction
        if not await check_before_play(interaction):
            return
        if vc.volume + 15 > 100:
            volume = 100
        else:
            volume = vc.volume + 15
        await vc.set_volume(volume)
        await nowplaying.np(self, self.interaction)
        try:
            await interaction.followup.send(content="")
        except:
            pass


class cl(Button):
    def __init__(self, interaction):
        super().__init__(
            emoji="<a:8_:989120444701491210>", style=discord.ButtonStyle.red
        )
        self.interaction = interaction

    async def callback(self, interaction):
        await interaction.response.defer()
        vc: wavelink.Player = interaction.guild.voice_client
        vc.interaction = interaction
        if not await check_before_play(interaction):
            return
        vc.queue.clear()
        await vc.skip()
        try:
            await interaction.followup.send(content="")
        except:
            pass


class dc(Button):
    def __init__(self, interaction):
        super().__init__(
            emoji="<a:7_:989120442851811359>", style=discord.ButtonStyle.red
        )
        self.interaction = interaction

    async def callback(self, interaction):
        await interaction.response.defer()
        vc: wavelink.Player = interaction.guild.voice_client
        vc.interaction = interaction
        if not await check_before_play(interaction):
            return
        if vc == None:
            return
        vc.queue.clear()
        c = vc.np
        vc.np = None
        try:
            await c.delete()
        except:
            pass
        await vc.disconnect()
        try:
            await interaction.followup.send(content="")
        except:
            pass


class au(Button):
    def __init__(self, interaction):
        super().__init__(
            emoji="<a:9_:989120446706364416>",
            style=discord.ButtonStyle.gray,
            custom_id="au",
        )
        self.interaction: discord.Interaction = interaction

    async def check_vip(self, v):
        if self.interaction.client.mango["vip"].find_one({"user_id": str(v)}):
            return True
        else:
            return False

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        vc: wavelink.Player = interaction.guild.voice_client
        vc.interaction = interaction
        respound = get_respound(interaction.locale, "callback")
        au = [x for x in vc.Myview.children if x.custom_id == "au"][0]
        if not await check_before_play(self.interaction):
            return
        if await self.check_vip(interaction.user.id):
            if vc.autoplay == wavelink.AutoPlayMode.partial:
                vc.autoplay = wavelink.AutoPlayMode.enabled
                au.style = discord.ButtonStyle.green
            elif vc.autoplay == wavelink.AutoPlayMode.enabled:
                vc.autoplay = wavelink.AutoPlayMode.partial
                au.style = discord.ButtonStyle.gray
            await nowplaying.np(self, self.interaction)
            try:
                await interaction.followup.send(content="")
            except:
                pass
        else:
            embed = createembed.callback(
                self.interaction, self.interaction.client, respound
            )
            await interaction.followup.send(embed=embed)


class nowplaying: 

    # async def np2(self, interaction, send=False):
    #     try:
    #         vc: wavelink.Player = interaction.guild.voice_client
    #         respound = get_respound(interaction.locale, "np")
    #         if vc:
    #             if vc.current is not None:
    #                 lists = vc.queue.copy()
    #                 upcoming = list(itertools.islice(lists, 1, 4))
    #                 fmt = "\n".join(
    #                     f'` {upcoming.index(_)+1}.{_["song"]} `' for _ in upcoming
    #                 )
    #                 if vc.queue[0].get("path") != None:
    #                     uri = None
    #                 else:
    #                     uri = f"https://www.youtube.com/watch?v={vc.current.data['info']['identifier']}"
    #                 npembed = discord.Embed(
    #                     title=f"{vc.current.data['info']['title']}  <a:blobdancee:969575788389220392>",
    #                     url=uri,
    #                     color=0xFFFFFF,
    #                 )
    #                 npembed.set_author(
    #                     name=f"{respound.get('nowplaying')} ❘ {vc.queue[0].get('source')}"
    #                 )
    #                 npembed.add_field(
    #                     name=f"{respound.get('playingin')}",
    #                     value=f"<#{interaction.guild.voice_client.channel.id}>",
    #                 )
    #                 npembed.add_field(
    #                     name=f"{respound.get('duration')}",
    #                     value=f"`{convert(vc.position)}/{convert(vc.current.data['info']['length'])}`",
    #                 )
    #                 npembed.set_footer(
    #                     text=f"{respound.get('addedby')} {vc.queue[0].get('requester').name} | {'Paused'if vc.is_paused() else 'Playing'} | {vc.volume}% | LoopStatus:{vc.loop} | Autoplay:{vc.autoplay}",
    #                     icon_url=f"{vc.queue[0].get('requester').avatar.url}",
    #                 )
    #                 try:
    #                     thumb = vc.queue[0]["song"].thumb
    #                 except:
    #                     thumb = "https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg?20200913095930"
    #                 npembed.set_image(url=thumb)
    #                 more = f"`{respound.get('andmore').format(more=len(lists)-4)}`"
    #                 if len(lists) - 4 <= 0:
    #                     more = None
    #                 if len(fmt) == 0:
    #                     fmt = f"`{respound.get('fmt')}`"
    #                 if send:
    #                     if more == None:
    #                         vc.np = await vc.interaction.followup.send(
    #                             content=f'**{respound.get("queue")}:**\n{fmt}',
    #                             embed=npembed,
    #                             view=vc.Myview,
    #                         )
    #                     else:
    #                         vc.np = await vc.interaction.followup.send(
    #                             content=f'**{respound.get("queue")}:**\n{fmt}\n{more}',
    #                             embed=npembed,
    #                             view=vc.Myview,
    #                         )
    #                     return
    #                 if vc.np:
    #                     try:
    #                         if more == None:
    #                             await vc.interaction.followup.edit_message(
    #                                 message_id=vc.np.id,
    #                                 content=f'**{respound.get("queue")}:**\n{fmt}',
    #                                 embed=npembed,
    #                                 view=vc.Myview,
    #                             )
    #                         else:
    #                             await vc.interaction.followup.edit_message(
    #                                 message_id=vc.np.id,
    #                                 content=f'**{respound.get("queue")}:**\n{fmt}\n{more}',
    #                                 embed=npembed,
    #                                 view=vc.Myview,
    #                             )
    #                     except:
    #                         if more == None:
    #                             vc.np = await vc.interaction.followup.send(
    #                                 content=f'**{respound.get("queue")}:**\n{fmt}',
    #                                 embed=npembed,
    #                                 view=vc.Myview,
    #                             )
    #                         else:
    #                             vc.np = await vc.interaction.followup.send(
    #                                 content=f'**{respound.get("queue")}:**\n{fmt}\n{more}',
    #                                 embed=npembed,
    #                                 view=vc.Myview,
    #                             )
    #                 else:
    #                     if more == None:
    #                         vc.np = await vc.interaction.followup.send(
    #                             content=f'**{respound.get("queue")}:**\n{fmt}',
    #                             embed=npembed,
    #                             view=vc.Myview,
    #                         )
    #                     else:
    #                         vc.np = await vc.interaction.followup.send(
    #                             content=f'**{respound.get("queue")}:**\n{fmt}\n{more}',
    #                             embed=npembed,
    #                             view=vc.Myview,
    #                         )
    #     except:
            # pass
    
     
    async def np(self,interaction, send=False):
            vc: wavelink.Player = interaction.guild.voice_client
            respound = get_respound(interaction.locale, "np")
            if vc:
                if vc.current is not None:
                    upcoming = list(itertools.islice(vc.queue,0, 4))
                    if vc.queue.mode == wavelink.QueueMode.loop_all:
                        upcoming = upcoming+list(vc.queue.history)
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
                        text=f"{'Paused'if not vc.playing else 'Playing'} | {vc.volume}% | LoopStatus:{trans_queueMode[f'wavelink.{str(vc.queue.mode)}']} | Autoplay:{trans_autoMode[f'wavelink.{str(vc.autoplay)}']}"
                    )

                    npembed.set_thumbnail(url=vc.current.artwork)
                    more = f"`{respound.get('andmore').format(more=len(vc.queue)-4)}`"
                    if len(vc.queue) - 4 <= 0:
                        more = None
                    if len(fmt) == 0:
                        fmt = f"`{respound.get('fmt')}`"
                    if send:
                        content = f'**{respound.get("queue")}:**\n{fmt}'f'\n{more}' if more else f'**{respound.get("queue")}:**\n{fmt}'
                        vc.np = await vc.interaction.followup.send(content=content, embed=npembed,view=vc.Myview )
                        return
                    if vc.np:
                        try:
                            content = f'**{respound.get("queue")}:**\n{fmt}'f'\n{more}' if more else f'**{respound.get("queue")}:**\n{fmt}'
                            vc.np = await vc.interaction.followup.edit_message(message_id=vc.np.id,content=content, embed=npembed,view=vc.Myview )
                        except:
                            content = f'**{respound.get("queue")}:**\n{fmt}'f'\n{more}' if more else f'**{respound.get("queue")}:**\n{fmt}'
                            vc.np = await vc.interaction.followup.edit_message(message_id=vc.np.id,content=content, embed=npembed,view=vc.Myview )
                    else:
                        content = f'**{respound.get("queue")}:**\n{fmt}'f'\n{more}' if more else f'**{respound.get("queue")}:**\n{fmt}'
                        vc.np = await vc.interaction.followup.send(content=content, embed=npembed,view=vc.Myview )
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
                client_id=self.bot.config.get("client_id"),
                client_secret=self.bot.config.get("client_secret"),
            )
        )
            
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
            embed = createembed.check_before_play(
                interaction, interaction.client, "novc", respound
            )
            await interaction.followup.send(embed=embed)
            return False
        if interaction.user.voice == None:
            embed = createembed.check_before_play(
                interaction, interaction.client, "usernotin", respound
            )
            await interaction.followup.send(embed=embed)
            return False
        if interaction.guild.voice_client.channel != interaction.user.voice.channel:
            embed = createembed.check_before_play(
                interaction, interaction.client, "diffchan", respound
            )
            await interaction.followup.send(embed=embed)
            return False
        return True

    @commands.Cog.listener()
    async def on_wavelink_track_exception(self, player: wavelink.Player, track, error):
        interaction: discord.Interaction = player.interaction
        vc: player = interaction.guild.voice_client
        respound = get_respound(interaction.locale, "callback")
        await asyncio.sleep(2)
        if vc.is_playing():
            await vc.stop()
        await vc.np.delete()
        vc.np = None
        await vc.stop()
        embed = createembed.on_wavelink_track_exception(
            interaction, interaction.client, respound
        )
        d = await interaction.followup_send(embed=embed)
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
            embed = createembed.baned(interaction, interaction.client, respound)
            d = await interaction.followup.send(embed=embed)
            await asyncio.sleep(5)
            await d.delete()
            return
        if await self.check_before_play(interaction):
            vc: wavelink.Player = interaction.guild.voice_client
            vc.interaction = interaction
            await nowplaying.np(self, interaction, send=True)

    @app_commands.command(
        name="autoplay",
        description="when ran out of music bot will random music for you",
    )
    async def autoplay(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if await self.check_ban(interaction.user.id):
            respound = get_respound(interaction.locale, "baned")
            embed = createembed.baned(interaction, interaction.client, respound)
            d = await interaction.followup.send(embed=embed)
            await asyncio.sleep(5)
            await d.delete()
            return
        vc.interaction = interaction
        vc: wavelink.Player = interaction.guild.voice_client
        respound = get_respound(interaction.locale, "callback")
        if await self.check_before_play(interaction):
            if await self.check_vip(interaction.user.id):
                if vc.autoplay == wavelink.AutoPlayMode.partial:
                    vc.autoplay = wavelink.AutoPlayMode.enabled
                elif vc.autoplay == wavelink.AutoPlayMode.enabled:
                    vc.autoplay = wavelink.AutoPlayMode.partial
                await nowplaying.np(self, self.interaction)
                try:
                    await interaction.response.send_message(content="")
                except:
                    pass
            else:
                embed = createembed.callback(
                    self.interaction, self.interaction.client, respound
                )
                await interaction.followup.send(embed=embed)

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
            embed = createembed.baned(interaction, interaction.client, respound)
            d = await interaction.followup.send(embed=embed)
            await asyncio.sleep(5)
            await d.delete()
            return
        
        respound = get_respound(interaction.locale, "check_before_play")

        if not interaction.user.voice:
            embed = createembed.check_before_play(interaction, interaction.client, "usernotin", respound)
            await interaction.followup.send(embed=embed)
            return
        
        elif not interaction.guild.voice_client:
            vc: wavelink.Player = await interaction.user.voice.channel.connect(cls=wavelink.Player)

        elif interaction.guild.voice_client.channel != interaction.user.voice.channel:
            embed = createembed.check_before_play(interaction, interaction.client, "diffchan", respound)
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
            pre = pr(interaction)
            pl = pp(interaction)
            loop = lo(interaction)
            skip = sk(interaction)
            # voldown = dw(interaction)
            # volup = uw(interaction)
            # clear = cl(interaction)
            auto = au(interaction)
            disconnect = dc(interaction)
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

        vc.interaction = interaction
        vc.autoplay = wavelink.AutoPlayMode.partial
        # -------Lplaylist
        if search == "Lplaylist":
            if await self.check_vip(interaction.user.id):
                database = self.bot.mango["lplaylist"]
                data = database.find_one({"user_id": str(interaction.user.id)})
                if not data:
                    respound = get_respound(interaction.locale, "callback")
                    embed = createembed.playnolplaylist(interaction, self.bot, respound)
                    await interaction.followup.send(embed=embed)
                    return
                first = None
                for title, uri in data["playlist"].items():
                    source = await createsource.searchen(
                        self,
                        uri.replace(self.replacer, self.replacement),
                        interaction,
                    )
                    if not first:
                        first = source
                    if not vc.queue and not vc.playing:
                        await vc.queue.put_wait(source)
                        await vc.play(await vc.queue.get_wait())
                    else:
                        await vc.queue.put_wait(source)
                        await nowplaying.np(self, interaction)
                        print(f'adding Lplaylist {source}')
                await self.addtoqueue(
                    first, interaction,playlist_title='Lplaylist', playlist=True, number=len(data["playlist"])
                )
                return
            else:
                respound = get_respound(interaction.locale, "callback")
                embed = createembed.noviplplaylist(interaction, self.bot, respound)
                await interaction.followup.send(embed=embed)
                return
        yt = False
        if "onlytube" in search:
            yt = True
            search = search.replace("onlytube", "")
        track = await createsource.searchen(self, search, interaction, onlyyt=yt)
        if track == None:
            embed = createembed.noresult(interaction, self.bot, respound)
            await interaction.followup.send(embed=embed)
            return
        
        if not vc.playing and not vc.queue:
            await vc.queue.put_wait(track)
            await vc.set_volume(100)
            await vc.play(await vc.queue.get_wait())
            print(f"playing {vc.current} requested by {vc.current.extras.requester}")
        else:
            await vc.queue.put_wait(track)
            print(f'adding {track}')
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
            source = database.find({"music": {"$regex": current}}).limit(25)
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
        while True:
            try:
                vc: wavelink.Player = vc.interaction.guild.voice_client
                np = await nowplaying.np(self,interaction)
                setattr(self.bot, "inter", interaction)
                setattr(self.bot, "re_np", np)
                await asyncio.sleep(9)
                if vc == None:
                    break
                if vc.np == None:
                    break
            except Exception as e:
                print(e)
            await asyncio.sleep(1)

    # --------------------------------

    async def corrected_song_name(self, title: str) -> str:
        st = self.bot.last.search_for_track("", title)
        searchtrack = st.get_next_page()
        if searchtrack:
            track = searchtrack[0]
            result = f"{track.title} - {track.artist} "
            print(f"last.fm | {title} -> {result}")
        else:
            corrected_title = self.sptf.search(q=title, type="track", limit=1)[
                "tracks"
            ]["items"]
            if corrected_title:
                track = corrected_title[0]
                result = f"{track['name']} - {track['artists'][0]['name']}"
                print(f"spotify | {title} -> {result}")
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
        print(f"Now playing : {vc.current}")
        vc.task = self.bot.loop.create_task(self.current_time(vc.interaction))

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload:wavelink.payloads.TrackEndEventPayload):
        print(f"ending: {payload.track}")
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
                embed = createembed.on_wavelink_track_end(
                    vc.interaction, self.bot, respound
                )
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
            print(f'counting no song {interaction.guild.name} | {i}')
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
            embed = createembed.baned(interaction, interaction.client, respound)
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
            embed = createembed.loop(interaction, self.bot, respound,trans_queueMode[status])
            d = await interaction.followup.send(embed=embed)
            await asyncio.sleep(5)
            await d.delete()

    @app_commands.command(name="resume", description="Resume music")
    async def resume(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if await self.check_ban(interaction.user.id):
            respound = get_respound(interaction.locale, "baned")
            embed = createembed.baned(interaction, interaction.client, respound)
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
            embed = createembed.resume(interaction, self.bot, respound)
            d = await interaction.followup.send(embed=embed)
            await asyncio.sleep(5)
            await d.delete()

    @app_commands.command(name="pause", description="Pause music")
    async def pause(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if await self.check_ban(interaction.user.id):
            respound = get_respound(interaction.locale, "baned")
            embed = createembed.baned(interaction, interaction.client, respound)
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
            embed = createembed.pause(interaction, self.bot, respound)
            d = await interaction.followup.send(embed=embed)
            await asyncio.sleep(5)
            await d.delete()

    @app_commands.command(name="skip", description="Skip music")
    @app_commands.describe(to="Skip to given music")
    async def skip(self, interaction: discord.Interaction, to: Optional[int] = False):
        await interaction.response.defer()
        if await self.check_ban(interaction.user.id):
            respound = get_respound(interaction.locale, "baned")
            embed = createembed.baned(interaction, interaction.client, respound)
            d = await interaction.followup.send(embed=embed)
            await asyncio.sleep(5)
            await d.delete()
            return
        if await self.check_before_play(interaction):
            vc: wavelink.Player = interaction.guild.voice_client
            vc.interaction = interaction
            if to:
                if to > len(vc.queue):
                    await interaction.followup.send("there is no queue index you provided.",ephemeral=True)
                wanted = vc.queue[to-1]
                await vc.queue.delete(to-1)
                await vc.play(wanted)
                respound = get_respound(interaction.locale, "skip")
                embed = createembed.skipto(interaction, self.bot, to, respound)
                d = await interaction.followup.send(embed=embed)
                await asyncio.sleep(5)
                await d.delete()
            else:
                await vc.skip()
                respound = get_respound(interaction.locale, "skip")
                embed = createembed.skip(interaction, self.bot, respound)
                d = await interaction.followup.send(embed=embed)
                await asyncio.sleep(5)
                await d.delete()

    @app_commands.command(name="shuffle", description="Shuffle music queue")
    async def shuffle(self, interaction: discord.Interaction):
        await interaction.response.defer()
        vc: wavelink.Player = interaction.guild.voice_client
        if await self.check_ban(interaction.user.id):
            respound = get_respound(interaction.locale, "baned")
            embed = createembed.baned(interaction, interaction.client, respound)
            d = await interaction.followup.send(embed=embed)
            await asyncio.sleep(5)
            await d.delete()
            return
        if await self.check_before_play(interaction):
            vc: wavelink.Player = interaction.guild.voice_client
            vc.interaction = interaction
            vc.queue.shuffle()
            respound = get_respound(interaction.locale, "shuffle")
            embed = createembed.shuffle(interaction, self.bot, respound)
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
            embed = createembed.baned(interaction, interaction.client, respound)
            d = await interaction.followup.send(embed=embed)
            await asyncio.sleep(5)
            await d.delete()
            return
        if await self.check_before_play(interaction):
            vc: wavelink.Player = interaction.guild.voice_client
            vc.interaction = interaction
            await self.cleanup(interaction.guild, "dc")
            respound = get_respound(interaction.locale, "dc")
            embed = createembed.dc(interaction, self.bot, respound)
            d = await interaction.followup.send(embed=embed)
            await asyncio.sleep(5)
            await d.delete()

    @app_commands.command(name="remove", description="Remove given music from queue")
    @app_commands.describe(index="Music Sequence")
    async def remove(self, interaction: discord.Interaction, index: int):
        await interaction.response.defer()
        if await self.check_ban(interaction.user.id):
            respound = get_respound(interaction.locale, "baned")
            embed = createembed.baned(interaction, interaction.client, respound)
            d = await interaction.followup.send(embed=embed)
            await asyncio.sleep(5)
            await d.delete()
            return
        if await self.check_before_play(interaction):
            vc: wavelink.Player = interaction.guild.voice_client
            vc.interaction = interaction
            delete = vc.queue._queue[index-1]
            respound = get_respound(interaction.locale, "remove")
            embed = createembed.remove(interaction, self.bot, delete, respound)
            await vc.queue.delete(index-1)
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
            respound = get_respound(interaction.locale, "remove_error")
            erembed = createembed.remove(interaction, self.bot, respound)
            await interaction.followup.send(embed=erembed)

    @app_commands.command(name="queue", description="Send queuelist")
    async def queueList(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if await self.check_ban(interaction.user.id):
            respound = get_respound(interaction.locale, "baned")
            embed = createembed.baned(interaction, interaction.client, respound)
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
            print(f'counting alonetime {member.guild.name} | {i}')
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
                        respound = get_respound(
                            lastone.guild.preferred_locale, "on_voice_state_update"
                        )
                        embed = createembed.on_voice_state_update2(
                            lastone, self.bot, respound
                        )
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
