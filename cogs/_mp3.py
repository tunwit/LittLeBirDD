import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice
from ui.embed_gen import createembed
from ui.language_respound import get_respound
from io import BytesIO
import yt_dlp
import tempfile
import threading
from queue import Queue
import os
from upload_to_drive import google_driveAPI
from discord.ui import View, Select
import asyncio
import time

class dow():
    def __init__(self,interaction:discord.Interaction,bot):
        self.bot = bot
        self.interaction = interaction
        self.progress = "0%"
        self.speed = "0KiB/s"
        self.title = None
        self.time = "Uncalculatable"
        self.complate = False
        self.data = None
        self.file_path = None
        self.fail = False
        self.ydl_opts = {
            'quiet': True,
            'ignoreerrors': True,
            'no_warnings': True,
            'noplaylist':True,
            'noprogress' : True,
            }
    

    async def update_message(self,respound):
        await self.interaction.edit_original_response(content=respound.get('progress').format(title=self.data['title'],progress=self.progress,speed=self.speed,time=self.time))

    def progress_hooks(self,d):
        if d['status'] == 'downloading':
            self.in_progress = True
            percent = str(round(float(d["_percent_str"].replace("%","")))) + "%"
            self.progress = percent
            self.time = d["_eta_str"]
            self.speed = d["_speed_str"]

        elif d['status'] == 'finished':
            percent = "100"
    
    def post_hooks(self,d:dict):
        self.file_path = d
        self.complate = True


    def dowload(self,url:str,queue,format,value,stop_event):
        with tempfile.NamedTemporaryFile(delete=False) as self.tempdirname:
            self.ydl_opts['outtmpl'] = f"{self.tempdirname.name}.%(ext)s"
            self.ydl_opts['progress_hooks'] = [self.progress_hooks]
            self.ydl_opts['post_hooks'] = [self.post_hooks]
            if format == "mp3 + mp4":
                self.ydl_opts["format"] = f'{value}+bestaudio'
            else:
                self.ydl_opts["format"] = value
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                for attemps in range(2):
                    try:
                        ydl.extract_info(url,download=True)
                        break
                    except yt_dlp.utils.DownloadError as e:
                        if attemps == 1:
                            self.fail = True
                            return
                while not self.complate:
                    time.sleep(0.5)
                pre, ext = os.path.splitext(self.file_path)
                newpath = pre +'.mp4'
                os.rename(self.file_path, newpath)
                queue.put(newpath)

class mp3API(commands.Cog):
    def __init__(self, bot):
        self.bot:commands.Bot = bot
    
    async def innitial_download(self,url,interaction:discord.Interaction,d:dow,data,format,value,resolution):
        queue = Queue()
        stop_event = threading.Event()
        respound = get_respound(interaction.locale,"mp3")
        await interaction.edit_original_response(content=respound.get('initializing'),view=None)
        await interaction.edit_original_response(content=respound.get('retriving').format(title=data['title']))
        process = threading.Thread(target=d.dowload, args=(url, queue,format,value,stop_event))
        process.start()
        await interaction.edit_original_response(content=respound.get('starting').format(title=data['title']))
        while not d.complate:
            if stop_event.is_set():
                raise yt_dlp.utils.DownloadError("Download cancelled by program.")
            if d.fail == True:
                await interaction.edit_original_response(content = respound.get('unexpected_error'))
                return
            await d.update_message(respound)
            await asyncio.sleep(1)
        process.join()
        file_path = queue.get()
        file_size = round(os.path.getsize(file_path) / 1000000,1)
        if file_size >= 8:
            await interaction.edit_original_response(content = respound.get('uploading_to_drive'))
            asyncio.ensure_future(google_driveAPI.upload_link(file_path,interaction,data['title'],respound))
        else:
            if format == "mp3 + mp4":
                format = "mp4"
            f = discord.File(fp=file_path,filename=f'{data["title"]}.{format}')
            await interaction.edit_original_response(content=respound.get('sending'))
            await interaction.edit_original_response(content=respound.get('successful'),attachments=[f])
        d.tempdirname.close()

    @app_commands.command(name="downloadmedia",description="dowload video from youtube as MP3 or MP4")
    @app_commands.describe(url="youtube video link")
    @app_commands.choices(file_type=[
    Choice(name = "MP3 (audio only)",value="mp3"),
    Choice(name = "MP4 (video only)",value="mp4"),
    Choice(name = "MP3 + MP4 (audio + video)",value="mp3 + mp4")])
    async def mp3(self,interaction:discord.Interaction,url:str,file_type:str):
        await interaction.response.defer()
        respound = get_respound(interaction.locale,"mp3")
        d = dow(interaction,self.bot)
        with yt_dlp.YoutubeDL() as ydl:
                data = ydl.extract_info(url,download=False)
                d.data = data
        opts = []
        if file_type == 'mp3':
            for streams in data["formats"]:
                if not (streams.get("acodec",None)==None and streams.get("vcodec",None)==None):
                    if streams.get("acodec")!="none" and streams.get("vcodec")=="none":
                        try:
                            opts.append(discord.SelectOption(label = f"Audio bitrate: {round(float(streams['abr']))}",value=streams['format_id']))
                        except:pass
        elif file_type == 'mp4':
            for streams in data["formats"]:
                if not (streams.get("acodec",None)==None and streams.get("vcodec",None)==None):
                    if streams.get("acodec")=="none" and streams.get("vcodec")!="none":
                        try:
                            opts.append(discord.SelectOption(label = f"Resolution: {streams['resolution']} Fps: {streams['fps']} Vbr: {round(float(streams['vbr']))}",value=streams['format_id']))
                        except:pass
        elif file_type == 'mp3 + mp4':
            for streams in data["formats"]:
                if not (streams.get("acodec",None)==None and streams.get("vcodec",None)==None):
                    if streams.get("vcodec")!="none":
                        try:
                            opts.append(discord.SelectOption(label = f"Resolution: {streams['resolution']} Fps: {streams['fps']} Vbr: {round(float(streams['vbr']))}",value=streams['format_id']))
                        except:pass
        opts.reverse()
        if len(opts) > 25:
            opts = opts[:25]

        select = Select(placeholder=respound.get("placeholder"),options=opts)
        async def callback_(interaction_:discord.Interaction):
            select.disabled = True
            for f in data['formats']:
                if f['format_id'] == select.values[0]:
                    resolution = f["format"]
                    break
            await self.innitial_download(url,interaction,d,data,file_type,select.values[0],resolution)

        select.callback = callback_
        v = View()
        v.add_item(select)
        await interaction.followup.send(view=v)


async def setup(bot):    
  await bot.add_cog(mp3API(bot))   