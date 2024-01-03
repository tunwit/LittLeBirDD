import discord
import time

class createembed:

    def reset_stats(interaction:discord.Interaction,bot,status:bool,respound:dict):
        if not status:
            embed = discord.Embed(title=f'{bot.user.name} | Reset_stats ❌ ', description=respound.get('failed'),color=0xCA1919)
            embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url)
        else:
            embed = discord.Embed(title=f'{bot.user.name} | Reset_stats ✅', description=respound.get('success'),color=0x19AD3B)
            embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url)
        return embed

    def setup_stats(interaction:discord.Interaction,bot,status:bool,respound:dict):
        if not status:
            embed = discord.Embed(title=f'{bot.user.name} | Setup_stats ❌ ', description=respound.get('failed'),color=0xCA1919)
            embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url)
        else:
            embed = discord.Embed(title=f'{bot.user.name} | Setup_stats ✅', description=respound.get('success'),color=0x19AD3B)
            embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url)
        return embed

    def setup_statsError(interaction:discord.Interaction,bot,respound:dict):
        embed = discord.Embed(title=f'{bot.user.name} | Setup_stats ❌ ', description=respound.get('failed'),color=0xCA1919)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url)
        return embed

    def check_before_play(interaction:discord.Interaction,bot,type:str,respound:dict):
        if type == "novc":
         embed = discord.Embed(title=f'{interaction.client.user.name} | {respound.get("failed")}', description=respound.get('novc'),color=0xCA1919)
         embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url)
        elif type == "usernotin":
         embed = discord.Embed(title=f'{interaction.client.user.name} | {respound.get("failed")}', description=respound.get('usernotin'),color=0xCA1919)
         embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url)
        elif type == "diffchan":
         embed = discord.Embed(title=f'{interaction.client.user.name} | {respound.get("failed")}', description=respound.get('diffchan'),color=0xCA1919)
         embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url)
        return embed
    
    def callback(interaction:discord.Interaction,bot,respound:dict):
        embed = discord.Embed(title=f'{interaction.client.user.name} | {respound.get("failed")}', description=respound.get('error'),color=0xCA1919)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url)
        return embed

    def on_wavelink_track_exception(interaction:discord.Interaction,bot,respound:dict):
        embed = discord.Embed(title=f'{bot.user.name} | {respound.get("failed")}', description=respound.get('on_wavelink_track_exception'),color=0xCA1919)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url)
        return embed

    def playnolplaylist(interaction:discord.Interaction,bot,respound:dict):
        embed = discord.Embed(title=f'{bot.user.name} | {respound.get("failed")}', description=respound.get('playnolplaylist'),color=0xCA1919)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed

    def noviplplaylist(interaction:discord.Interaction,bot,respound:dict):
        embed = discord.Embed(title=f'{bot.user.name} | {respound.get("failed")}', description=respound.get('error'),color=0xCA1919)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed
    
    def noresult(interaction:discord.Interaction,bot,respound:dict):
        embed = discord.Embed(title=f'{bot.user.name} | {respound.get("failed")}', description=respound.get('noresult'),color=0xCA1919)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed

    def on_wavelink_track_end(interaction:discord.Interaction,bot,respound:dict):   
        embed = discord.Embed(title=f'{bot.user.name} | {respound.get("failed")}', description=respound.get('error'),color=0xCA1919)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed

    def loop(interaction:discord.Interaction,bot,respound:dict,loop):   
        embed = discord.Embed(title=f'{bot.user.name} | Loop ✅ ', description=f"{respound.get('loopchanged')} **`{loop}`**",color=0x19AD3B)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed

    def resume(interaction:discord.Interaction,bot,respound:dict):   
        embed = discord.Embed(title=f'{bot.user.name} | Resume ✅ ', description=respound.get('resumed'),color=0x19AD3B)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed

    def pause(interaction:discord.Interaction,bot,respound:dict):   
        embed = discord.Embed(title=f'{bot.user.name} | Pause ✅ ', description=respound.get('paused'),color=0x19AD3B)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed
    
    def skip(interaction:discord.Interaction,bot,respound:dict):
        embed = discord.Embed(title=f'{bot.user.name} | Skip ✅ ', description=respound.get('skiped'),color=0x19AD3B)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed
    
    def skipto(interaction:discord.Interaction,bot,to,respound:dict):
        embed = discord.Embed(title=f'{bot.user.name} | Skip to ✅ ', description=respound.get('skipedto').format(to=to),color=0x19AD3B)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed

    def dc(interaction:discord.Interaction,bot,respound:dict):
        embed = discord.Embed(title=f'{bot.user.name} | Disconnect ✅ ', description=respound.get('dced'),color=0x19AD3B)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed

    def remove(interaction:discord.Interaction,bot,deleted,respound:dict):
        embed = discord.Embed(title=f'{bot.user.name} | Remove ✅', description=respound.get('removed').format(deleted=deleted),color=0x19AD3B)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed

    def shuffle(interaction:discord.Interaction,bot,respound:dict):
        embed = discord.Embed(title=f'{bot.user.name} | shuffle ✅', description=respound.get('shuffle'),color=0x19AD3B)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed

    def on_voice_state_update(member:discord.Member,bot,respound:dict):
        embed = discord.Embed(title=f"{bot.user.name} | {respound.get('kick?')}", description=respound.get('descript'),color=0xCA1919)
        embed.set_footer(text = f"{respound.get('requester').format(user=member.name)}", icon_url=member.avatar.url) 
        return embed
    
    def on_voice_state_update2(member:discord.Member,bot,respound:dict):
        embed = discord.Embed(title=f"{bot.user.name} | {respound.get('noone')}", description=respound.get('descript2'),color=0xCA1919)
        embed.set_footer(text = f"{respound.get('requester').format(user=member.name)}", icon_url=member.avatar.url) 
        return embed
    
    def toggle_lv(interaction:discord.Interaction,bot,result,respound:dict):
        embed = discord.Embed(title=f'{bot.user.name} | Toggle_leveling ✅', description=respound.get('descript').format(result=result),color=0x19AD3B)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed

    def gif(interaction:discord.Interaction,bot,respound:dict):
        embed=discord.Embed(title=f"{bot.user.name} | {respound.get('failed')}",description={respound.get('descript')},color=0xCA1919)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed
    
    def anime(interaction:discord.Interaction,bot,respound:dict,nsfw=False):
        if nsfw:
            embed=discord.Embed(title=f"{bot.user.name} | {respound.get('failed')}",description=respound.get('nsfw'),color=0xCA1919)
            embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        else:
            embed=discord.Embed(title=f"{bot.user.name} | {respound.get('failed')}",description=respound.get('descript'),color=0xCA1919)
            embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed
    
    def addplaylistnoresult(interaction:discord.Interaction,bot,respound:dict):
        embed = discord.Embed(title=f"{bot.user.name} | {respound.get('failed')}", description=respound.get('noresult'),color=0xCA1919)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed
    
    def addplaylistsuccess(interaction:discord.Interaction,bot,respound:dict,title):
        embed = discord.Embed(title=f"{bot.user.name} | Addplaylist ✅", description=respound.get('success').format(title=title),color=0x19AD3B)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed

    def addplaylistnovip(interaction:discord.Interaction,bot,respound:dict):
        embed = discord.Embed(title=f"{bot.user.name} | {respound.get('failed')}", description=respound.get('notvip'),color=0xCA1919)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed

    def ql_playlistnolist(interaction:discord.Interaction,bot,respound:dict):
        embed = discord.Embed(title=f'{bot.user.name} | Ql_playlist ❌ ', description=respound.get('nolist'),color=0xCA1919)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed

    def ql_playlistsuccess(interaction:discord.Interaction,bot,respound:dict,fmt):
        embed = discord.Embed(title=f'{bot.user.name} | Ql_playlist ✅ ', description=respound.get('success').format(fmt=fmt),color=0x19AD3B)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed

    def ql_playlistnovip(interaction:discord.Interaction,bot,respound:dict):
        embed = discord.Embed(title=f'{bot.user.name} | Ql_playlist ❌ ', description=respound.get('notvip'),color=0xCA1919)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed

    def remove_playlistnolist(interaction:discord.Interaction,bot,respound:dict):
        embed = discord.Embed(title=f'{bot.user.name} | Remove_playlist ❌ ', description=respound.get('nolist'),color=0xCA1919)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed

    def remove_playlistsuccess(interaction:discord.Interaction,bot,respound:dict,title):
        embed = discord.Embed(title=f'{bot.user.name} | Remove_playlist ✅ ', description=respound.get('success').format(title=title),color=0x19AD3B)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed

    def remove_playlistnovip(interaction:discord.Interaction,bot,respound:dict):
        embed = discord.Embed(title=f'{bot.user.name} | Remove_playlist ❌ ', description=respound.get('notvip'),color=0xCA1919)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed

    def remove_playlist_error(interaction:discord.Interaction,bot,respound:dict):
        embed=discord.Embed(title=f"{bot.user.name} | {respound.get('failed')}",description=respound.get('descript'),color=0xCA1919)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed
    
    def clear_playlistsuccess(interaction:discord.Interaction,bot,respound:dict):
        embed = discord.Embed(title=f'{bot.user.name} | Clear_playlist ✅ ', description=respound.get('success'),color=0x19AD3B)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed

    def clear_playlistfailed(interaction:discord.Interaction,bot,respound:dict):
        embed = discord.Embed(title=f'{bot.user.name} | Clear_playlist ❌ ', description=respound.get('failed'),color=0xCA1919)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed

    def cr_clearsuccess(interaction:discord.Interaction,bot,respound:dict):
        embed=discord.Embed(title=f"{bot.user.name} | {respound.get('success')}",description={respound.get('descript')},color=0xE5583F)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed
    
    def cr_listnolist(interaction:discord.Interaction,bot,respound:dict):
        embed = discord.Embed(title=f'{respound.get("nolist")}', description=respound.get("descript"),color=0xE5583F)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed

    def cr_removefailed(interaction:discord.Interaction,bot,respound:dict):
        embed = discord.Embed(title=f'{bot.user.name} | {respound.get("failed")}', description=respound.get("descript"),color=0xCA1919)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed

    def cr_randomnolist(interaction:discord.Interaction,bot,respound:dict):
        embed=discord.Embed(title=f"{bot.user.name} | {respound.get('failed')}",description=respound.get("nolist"),color=0xCA1919)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed

    def remove_error(interaction:discord.Interaction,bot,respound:dict):
        embed=discord.Embed(title=f"{bot.user.name} | {respound.get('failed')}",description=respound.get("descript"),color=0xCA1919)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed

    def lyrics(interaction:discord.Interaction,bot,respound:dict):
        embed=discord.Embed(title=f"{bot.user.name} |{respound.get('failed')}",description=respound.get("descript"),color=0xCA1919)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed

    def filters(interaction:discord.Interaction,bot,respound:dict,type):
        embed=discord.Embed(title=f"{bot.user.name} |{respound.get('title')}",description=respound.get(type),color=0x19AD3B)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed
    
    def baned(interaction:discord.Interaction,bot,respound:dict):
        embed=discord.Embed(title=f"{bot.user.name} |{respound.get('title')}",description=respound.get('descript'),color=0xCA1919)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed
    
    def set_welcome(interaction:discord.Interaction,bot,respound:dict):
        embed=discord.Embed(title=f"{bot.user.name} |{respound.get('title')}",description=respound.get('descript'),color=0x19AD3B)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed

    def unset_welcome(interaction:discord.Interaction,bot,respound:dict):
        embed=discord.Embed(title=f"{bot.user.name} |{respound.get('success')}",description=respound.get('descript'),color=0x19AD3B)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed
    
    def unset_welcome_error(interaction:discord.Interaction,bot,respound:dict):
        embed=discord.Embed(title=f"{bot.user.name} |{respound.get('failed')}",description=respound.get('descript_fail'),color=0x19AD3B)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed

    def set_track(interaction:discord.Interaction,bot,respound:dict,channel:str):
        embed=discord.Embed(title=f"{bot.user.name} |{respound.get('title')}",description=respound.get('descript').format(channel=channel),color=0x19AD3B)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed

    def joinvc(respound:dict,member:discord.Member,channel):
        embed=discord.Embed(description=respound.get('join').format(user=member.display_name,channel=channel),color=0x19AD3B)
        embed.set_author(name=member.name+member.discriminator,icon_url=member.display_avatar.url)
        embed.set_footer(text = time.strftime("%D | %H:%M:%S")) 
        return embed
    
    def leavevc(respound:dict,member:discord.Member,channel):
        embed=discord.Embed(description=respound.get('leave').format(user=member.display_name,channel=channel),color=0xcc8c2d)
        embed.set_author(name=member.name+member.discriminator,icon_url=member.display_avatar.url)
        embed.set_footer(text = time.strftime("%D | %H:%M:%S")) 
        return embed
    
    def movevc(respound:dict,member:discord.Member,channel1,channel2):
        embed=discord.Embed(description=respound.get('moveto').format(user=member.display_name,channel1=channel1,channel2=channel2),color=0x2bc2b3)
        embed.set_author(name=member.name+member.discriminator,icon_url=member.display_avatar.url)
        embed.set_footer(text = time.strftime("%D | %H:%M:%S")) 
        return embed 
    def invalid_format(interaction:discord.Interaction,bot,respound:dict):
        embed = discord.Embed(title=f"{bot.user.name} | {respound.get('failed')}", description=respound.get('descript'),color=0xCA1919)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed 
    
    def set_reminder_com(interaction:discord.Interaction,bot,respound:dict,_time,message):
        embed=discord.Embed(title=f"{bot.user.name} |{respound.get('set_remind_com')}",description=respound.get('set_remind_com_des').format(time=_time,message=message),color=0x19AD3B)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed
    
    def foretime(interaction:discord.Interaction,bot,respound:dict):
        embed=discord.Embed(title=f"{bot.user.name} |{respound.get('failed')}",description=respound.get('desfprtime'),color=0xCA1919)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url) 
        return embed 
    
    def reminder(user:discord.User,bot,respound:dict,message):
        embed = discord.Embed(title=f"{bot.user.name} | {respound.get('reminder')}", description=f"<@{user.id}>   ``{message}``",color=0x408a2c)
        embed.set_footer(text = f"{respound.get('requester').format(user=user.name)}", icon_url=user.avatar.url) 
        return embed 