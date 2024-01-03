import discord
from discord.ext import tasks,commands
import json
from discord import app_commands
from discord.app_commands import Choice
import asyncio
from ui.language_respound import get_respound
from ui.embed_gen import createembed
from discord.ui import View, Button , button , Select
import random
import copy


class villager():
    def __init__(self,who,paired,game,message=None):
        self.who=who
        self.paired=paired
        self.game=game
        self.voted = None
        self.message = message
    
    async def sendmessage(self,interaction):
        pass

class werewolf():
    def __init__(self,who,paired,game,message=None):
        self.who=who
        self.paired=paired
        self.game=game
        self.voted = None
        self.message = message

    def get_optionlist(self):
        options = []
        for u in self.paired:
            if u[0] != self.who:
                if u[1].__class__.__name__ != self.__class__.__name__ :  
                    option = discord.SelectOption(label=u[0].name,description=f"Vote to kill {u[0].name}")
                    options.append(option)
        return options
    
    async def sendmessage(self,interaction:discord.Interaction):
        select = Select(placeholder="vote for the one u want to kill",options=self.get_optionlist())
        view = View()
        view.add_item(select)
        i = [i[1]+":"+i[0] for i in self.game.werewolfwanttokill.copy()]
        update = '\n'.join(i)
        embed = discord.Embed(title="werewolf",description=f"`{update}`")
        async def my_callback(interaction:discord.Interaction):
            select.disabled=True
            self.game.werewolfwanttokill.append([select.values[0],self.who.name])
            i = [i[1]+":"+i[0] for i in self.game.werewolfwanttokill.copy()]
            update = '\n'.join(i)
            embed = discord.Embed(title="werewolf",description=f"`{update}`")
            await self.message.edit(embed=embed,view=view)
            await interaction.response.send_message(f"You voted to {select.values[0]}")
            await self.game.updatewwvote()
        select.callback = my_callback
        message = await self.who.send(embed=embed,view=view)
        self.message = message
        return self.message


class seer():
    def __init__(self,who,paired,game,message=None):
        self.who=who
        self.paired=paired
        self.game=game
        self.voted = None
        self.message = message

    def get_optionlist(self):
        options = []
        for u in self.paired:
            if u[0] != self.who:
                option = discord.SelectOption(label=u[0].name,description=f"Vote to interact {u[0].name}")
                options.append(option)
        return options
    
    async def sendmessage(self,interaction):
        select = Select(placeholder="Select for the one u want to interact",options=self.get_optionlist())
        view = View()
        view.add_item(select)
        async def my_callback(interaction):
            select.disabled=True
            target = None
            for u in self.paired:
                if u[0].name == select.values[0]:
                    target = u[1].__class__.__name__
                    break
            await self.message.edit(view=view)
            await interaction.response.send_message(f"{select.values[0]} is {target}")
        select.callback = my_callback
        self.message = await self.who.send(view=view)

class bodygard():
    def __init__(self,who,paired,game,message=None):
        self.who=who
        self.paired=paired
        self.game=game
        self.voted = None
        self.message = message

    def get_optionlist(self):
        options = []
        for u in self.paired:
            if u[0] != self.who:
                option = discord.SelectOption(label=u[0].name,description=f"Select to protect {u[0].name}")
                options.append(option)
        return options
    
    async def sendmessage(self,interaction):
        select = Select(placeholder="Select for the one u want to protect",options=self.get_optionlist())
        view = View()
        view.add_item(select)
        async def my_callback(interaction):
            select.disabled=True
            target = None
            for u in self.paired:
                if u[0].name == select.values[0]:
                    target = u
                    break
            await self.message.edit(view=view)
            await interaction.response.send_message(f"You are protecting {target[0].name}")
        select.callback = my_callback
        self.message = await self.who.send(view=view)
        
class idiot():
    def __init__(self,who,paired,game,message=None):
        self.who=who
        self.paired=paired
        self.game=game
        self.voted = None
        self.message = message
    
    async def sendmessage(self,interaction):
        pass

class game(View):
    def __init__(self,owner,interaction,bot):
        super().__init__(timeout=None)
        self.bot = bot
        self.players=[]
        self.owner = owner
        self.interaction = interaction
        self.origin = None
        self.children[1].style = discord.ButtonStyle.red
        self.children[1].disabled = True
        self.roless = ["werewolf","werewolf","seer"]
        self.paired = []
        self.task = None
        self.timefdisscuss = 10
        self.nighttime = 10
        self.werewolfwanttokill =[]

    def roles(self):
        player = len(self.players)
        role = []
        if player <= 7:
            werewolf = round(player/4)
            seer = round(player/6)
            bodygard = round(player/5)
            villager = player-(werewolf+seer+bodygard)
        else:
            werewolf = round(player/3)
            seer = round(player/6)
            bodygard = round(player/5)
            idiot = round(player/7.5)
            villager = player-(werewolf+seer+bodygard)   
            for i in range(idiot):
                self.roless.append("idiot")
        for i in range(werewolf):
            role.append("werewolf")
        for i in range(seer):
            role.append("seer")
        for i in range(bodygard):
            role.append("bodygard")
        for i in range(villager):
            role.append("villager")
        random.shuffle(role)
        return role

    def pair(self):
        p = []
        for i in range(len(self.players)):
            who = self.players[i]
            paired = None
            p.append([self.players[i],eval(self.roless[i]+"(who,paired,self)")])
        return p
    
    def setvariable(self):
        for i in self.paired:
            i[1].paired = self.paired

    def initualize(self,interaction:discord.Interaction):
        # self.roless = self.roles()
        self.paired = self.pair()
        self.setvariable()
   
    async def check(self,interaction:discord.Interaction):
        if interaction.user.id != self.owner.id:
            await interaction.followup.send("Only the host can start the game",ephemeral=True)
            return False
        return True
    
    async def updatewwvote(self):
        for i in self.paired:
            u = [i[1]+":"+i[0] for i in self.werewolfwanttokill.copy()]
            update = '\n'.join(u)
            embed = discord.Embed(title="werewolf",description=f"`{update}`")
            try:
                await i[2].edit(embed=embed)
            except:pass

#-------------started        
    @tasks.loop(seconds=1)
    async def timefdiss(self): 
         await self.origin.edit(content=f"Game has been started lets talk time'sup in `{self.timefdisscuss}`",view=None,embed=None)
         if self.timefdisscuss == 0:
            self.timefdiss.cancel()
            self.timefdisscuss = 10
         self.timefdisscuss -=1

    @timefdiss.after_loop
    async def afterday(self):
        self.night.start()
        for i in self.paired:
            message = await i[1].sendmessage(self.interaction)   
            i.append(message)
            await asyncio.sleep(0.5)

#-------------nighttime      
    @tasks.loop(seconds=1)    
    async def night(self):
        await self.origin.edit(content=f"Now its night time ,Sun will raise in {self.nighttime}",view=None,embed=None)
        if self.nighttime == 0:
            self.night.cancel()
            self.nighttime = 10
        self.nighttime -=1

    @night.after_loop
    async def afternight(self):
        print("afternight")
        lst = []
        for i in self.werewolfwanttokill:   
            lst.append(i)
        killed = max(set(lst), key = lst.count)
        print(killed)

#-------------start       
    async def start(self):
        for i in self.paired:
            partner = []
            for u in self.paired:
                if type(u[1]).__name__ == type(i[1]).__name__ :
                    if u[0] is not i[0]:
                        partner.append(u[0].name)
            await i[0].send(f"You are {type(i[1]).__name__} your partner is {' '.join(partner)}")
        self.timefdiss.start()

    @button(label="Join",style=discord.ButtonStyle.blurple)
    async def jo(self,interaction:discord.Interaction,button):
        await interaction.response.defer()
        try:
            await interaction.followup.send("")
        except:
            pass
        if interaction.user in self.players:
            await interaction.followup.send("you are already in the game",ephemeral=True)
        else:
            if len(self.players) > 15:
                await interaction.followup.send("Max 15 people u can not play",ephemeral=True)
                return
            self.players.append(interaction.user)
            await interaction.followup.send("you are joined the game",ephemeral=True)
            if len(self.players)>=1:
                self.children[1].style = discord.ButtonStyle.green
                self.children[1].disabled = False
        embed = discord.Embed(title = "Were wolf has been start\nReact to button to Join ")
        embed.add_field(name="Joined",value=' '.join(f"<@{line.id}>" for line in self.players))
        await self.origin.edit(embed=embed,view=self)

    @button(label="Start",style=discord.ButtonStyle.red)
    async def st(self,interaction:discord.Interaction,button):
        await interaction.response.defer()
        try:
            await interaction.followup.send("")
        except:
            pass
        if await self.check(interaction):
            if len(self.players)<1 :
                await interaction.followup.send("Only started the game when atleast 5 player and maximum with 15",ephemeral=True)
            else:
                self.initualize(interaction)
                await self.start()


class ww(commands.Cog):
  def __init__(self,bot):
     self.bot = bot

  @app_commands.command(name="werewolf",description="Play werewolf")
  async def werewolf(self,interaction:discord.Interaction):
    await interaction.response.defer()
    view = game(interaction.user,interaction,self.bot)
    view.players.append(interaction.user)
    embed:discord.Embed = discord.Embed(title = "Were wolf has been start\nReact to button to Join ")
    embed.add_field(name="Joined",value=' '.join(f"<@{line.id}>" for line in view.players))
    origin = await interaction.followup.send(embed=embed,view=view)
    view.origin=origin


async def setup(bot):
  await bot.add_cog(ww(bot))