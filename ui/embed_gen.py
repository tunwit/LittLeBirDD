import discord
import time

class createembed:
    
    def embed_success(interaction:discord.Interaction,respound:dict,formatter=''):
        embed = discord.Embed(title=f'{interaction.client.user.name} | {respound["success_title"]} ', description=respound.get('success_description').format(formatter),color=0x19AD3B)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url)
        return embed
    
    def embed_fail(interaction:discord.Interaction,respound:dict,formatter=''):
        embed = discord.Embed(title=f'{interaction.client.user.name} | {respound["failed_title"]} ', description=respound.get('failed_description').format(formatter),color=0xCA1919)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url)
        return embed
    
    def embed_info(interaction:discord.Interaction,respound:dict,formatter=''):
        embed = discord.Embed(title=f'{interaction.client.user.name} | {respound["info_title"]} ', description=respound.get('info_description').format(formatter),color=0xf2dd3a)
        embed.set_footer(text = f"{respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url)
        return embed
    
    def reminder(user:discord.User,bot:discord.Client,respound:dict,message):
        embed = discord.Embed(title=f"{bot.user.name} | {respound.get('reminder')}", description=f"<@{user.id}>   ``{message}``",color=0x408a2c)
        embed.set_footer(text = f"{respound.get('requester').format(user=user.name)}", icon_url=user.avatar.url) 
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
