import wavelink as wavelink
from discord.ext import commands
import requests
import discord

class createsource(commands.Cog):
 def __init__(self, bot ):
    self.bot = bot

 async def searchen(self,search,interaction:discord.Interaction,artist=None,onlyyt=False):
        result = await wavelink.Playable.search(search,source=wavelink.TrackSource.YouTube if onlyyt else wavelink.TrackSource.YouTubeMusic)
        if not result:
           return None
        if isinstance(result,wavelink.Playlist):
            if result.selected == -1:
               result.track_extras()
               for track in result.tracks:
                  track.extras = {'requester': interaction.user.name,'requester_icon' : interaction.user.avatar.url}
               song = result
            else:
              result.tracks[result.selected].extras = {'requester': interaction.user.name,'requester_icon' : interaction.user.avatar.url,"thumb":result.tracks[result.selected].artwork}
              song = result.tracks[result.selected]
        else:
           song = result[0]
           song.extras = {'requester': interaction.user.name,'requester_icon' : interaction.user.avatar.url,'source':'youtube',"thumb":song.artwork}

        return  song
 
async def setup(bot):    
  await bot.add_cog(createsource(bot))  