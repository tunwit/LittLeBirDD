import discord
from discord.ext import commands
import json
from discord import app_commands
from discord.app_commands import Choice
import asyncio
from ui.language_respound import get_respound
from ui.embed_gen import createembed
from discord.ui import View, Button , button
import random

class again(View):
    def __init__(self,fp,sp,interaction,origin):
        super().__init__()
        self.fp = fp
        self.sp = sp
        self.interaction = interaction
        self.origin = origin

    async def check(self,interaction:discord.Interaction):
        if interaction.user.id != self.fp.id and interaction.user.id != self.sp.id :
            await interaction.followup.send("Dosen't talk to you idiot!",ephemeral=True)
            return False
        return True

    def get_p(self,interaction):
        if interaction.user == self.fp:
            return self.sp
        else:
            return self.fp

    @button(label="Playagain?",style=discord.ButtonStyle.green)
    async def ac(self,interaction:discord.Interaction,button):
        await interaction.response.defer()
        if await self.check(interaction):
            try:
                await interaction.followup.send("")
            except:
                pass
            x=xo(self.get_p(interaction),interaction)
            await self.origin.edit(content=f"🎲 `{x.fp[0].name}` VS `{x.sp[0].name}`\n\n <@{x.current[0].id}> ,Its yours Turn",embed=None,view=x)
            x.origin = self.origin

    @button(label="Close",style=discord.ButtonStyle.red)
    async def de(self,interaction:discord.Interaction,button):
        await interaction.response.defer()
        if await self.check(interaction):
            try:
                await interaction.followup.send("")
            except:
                pass
            await self.origin.delete()

class xo(View):
    def __init__(self,opponent,interaction):
        super().__init__()
        self.origin = None
        self.xo = ["X","O"]
        self.player = [opponent,interaction.user]
        self.interaction:discord.Interaction = interaction
        self.fp = self.getfp()
        self.sp = self.getsp()
        self.current = None
        self.first = self.getfirst()
        self.win = [
            {1,2,3},
            {4,5,6},
            {7,8,9},
            {1,4,7},
            {2,5,8},
            {3,6,9},
            {1,5,9},
            {3,5,7}
        ]
        self.fpplased = set()
        self.spplased = set()
        self.gameover = False
        self.count = 0
    
    async def update(self,interaction:discord.Interaction):
        if self.gameover == False:
         self.getnext()
         await self.origin.edit(content=f"🎲 `{self.fp[0].name}` VS `{self.sp[0].name}`\n\n<@{self.current[0].id}> ,Its yours Turn",view=self)
        else:
         for i in self.children:
            i.disabled=True
         if self.gameover == "tie":
             await self.origin.edit(content=f"No one won the game try again?",view=self)
         else:
             await self.origin.edit(content=f"🎉 `{self.fp[0].name}` VS `{self.sp[0].name}`\n\n<@{self.current[0].id}> ,has won the round!",view=self)
         view = again(self.fp[0],self.sp[0],interaction,self.origin)
         await self.origin.edit(view=view)
         self.stop()

    def getfirst(self):
        first = random.choice([self.fp,self.sp])
        self.current = first
        return first

    def getfp(self):
        fp = random.choice(self.player)
        self.player.remove(fp)
        xo = random.choice(self.xo)
        self.xo.remove(xo)
        return [fp,xo]

    def getsp(self):
        sp = self.player[0]
        xo = self.xo[0]
        return [sp,xo]

    def getnext(self):    
        if self.current == self.sp:
            self.current = self.fp
        elif self.current == self.fp:
            self.current = self.sp
            
    async def check(self,interaction:discord.Interaction):
        if interaction.user.id != self.current[0].id:
            await interaction.followup.send("Not your turn, You idiot!",ephemeral=True)
            return False
        return True

    def checkwin(self):
        self.count += 1
        if self.count >= 9 :
            self.gameover = "tie"
            
        for i in self.win:
            if i.issubset(self.fpplased) or i.issubset(self.spplased):
                self.gameover = True

    @button(label="-",style=discord.ButtonStyle.gray,row=0)
    async def one(self,interaction:discord.Interaction,button):
        await interaction.response.defer()
        if await self.check(interaction):
            button.label = self.current[1]
            button.style = discord.ButtonStyle.danger if self.current[1] =="X" else discord.ButtonStyle.blurple
            button.disabled=True
            if self.current == self.fp:
                self.fpplased.add(1)
            else:
                self.spplased.add(1)
            self.checkwin()
            await self.update(interaction)

    @button(label="-",style=discord.ButtonStyle.gray,row=0)
    async def two(self,interaction:discord.Interaction,button):
        await interaction.response.defer()
        if await self.check(interaction):
            button.label = self.current[1]
            button.style = discord.ButtonStyle.danger if self.current[1] =="X" else discord.ButtonStyle.blurple
            button.disabled=True
            if self.current == self.fp:
                self.fpplased.add(2)
            else:
                self.spplased.add(2)
            self.checkwin()
            await self.update(interaction)

    @button(label="-",style=discord.ButtonStyle.gray,row=0)
    async def three(self,interaction:discord.Interaction,button):
        await interaction.response.defer()
        if await self.check(interaction):
            button.label = self.current[1]
            button.style = discord.ButtonStyle.danger if self.current[1] =="X" else discord.ButtonStyle.blurple
            button.disabled=True
            if self.current == self.fp:
                self.fpplased.add(3)
            else:
                self.spplased.add(3)
            self.checkwin()
            await self.update(interaction)

    @button(label="-",style=discord.ButtonStyle.gray,row=1)
    async def four(self,interaction:discord.Interaction,button):
        await interaction.response.defer()
        if await self.check(interaction):
            button.label = self.current[1]
            button.style = discord.ButtonStyle.danger if self.current[1] =="X" else discord.ButtonStyle.blurple
            button.disabled=True
            if self.current == self.fp:
                self.fpplased.add(4)
            else:
                self.spplased.add(4)
            self.checkwin()
            await self.update(interaction)

    @button(label="-",style=discord.ButtonStyle.gray,row=1)
    async def five(self,interaction:discord.Interaction,button):
        await interaction.response.defer()
        if await self.check(interaction):
            button.label = self.current[1]
            button.style = discord.ButtonStyle.danger if self.current[1] =="X" else discord.ButtonStyle.blurple
            button.disabled=True
            if self.current == self.fp:
                self.fpplased.add(5)
            else:
                self.spplased.add(5)
            self.checkwin()
            await self.update(interaction)

    @button(label="-",style=discord.ButtonStyle.gray,row=1)
    async def six(self,interaction:discord.Interaction,button):
        await interaction.response.defer()
        if await self.check(interaction):
            button.label = self.current[1]
            button.style = discord.ButtonStyle.danger if self.current[1] =="X" else discord.ButtonStyle.blurple
            button.disabled=True
            if self.current == self.fp:
                self.fpplased.add(6)
            else:
                self.spplased.add(6)
            self.checkwin()
            await self.update(interaction)

    @button(label="-",style=discord.ButtonStyle.gray,row=2)
    async def seven(self,interaction:discord.Interaction,button):
        await interaction.response.defer()
        if await self.check(interaction):
            button.label = self.current[1]
            button.style = discord.ButtonStyle.danger if self.current[1] =="X" else discord.ButtonStyle.blurple
            button.disabled=True
            if self.current == self.fp:
                self.fpplased.add(7)
            else:
                self.spplased.add(7)
            self.checkwin()
            await self.update(interaction)

    @button(label="-",style=discord.ButtonStyle.gray,row=2)
    async def eight(self,interaction:discord.Interaction,button):
        await interaction.response.defer()
        if await self.check(interaction):
            button.label = self.current[1]
            button.style = discord.ButtonStyle.danger if self.current[1] =="X" else discord.ButtonStyle.blurple
            button.disabled=True
            if self.current == self.fp:
                self.fpplased.add(8)
            else:
                self.spplased.add(8)
            self.checkwin()
            await self.update(interaction)

    @button(label="-",style=discord.ButtonStyle.gray,row=2)
    async def nine(self,interaction:discord.Interaction,button):
        await interaction.response.defer()
        if await self.check(interaction):
            button.label = self.current[1]
            button.style = discord.ButtonStyle.danger if self.current[1] =="X" else discord.ButtonStyle.blurple
            button.disabled=True
            if self.current == self.fp:
                self.fpplased.add(9)
            else:
                self.spplased.add(9)
            self.checkwin()
            await self.update(interaction)

class Accept(View):
    def __init__(self,opponent,interaction):
        super().__init__()
        self.opponent = opponent
        self.interaction = interaction
        self.origin = None

    async def check(self,interaction:discord.Interaction):
        if interaction.user.id != self.opponent.id:
            await interaction.followup.send("Dosen't talk to you idiot!",ephemeral=True)
            return False
        return True

    @button(label="Accept",style=discord.ButtonStyle.green)
    async def ac(self,interaction:discord.Interaction,button):
        await interaction.response.defer()
        if await self.check(interaction):
            try:
                await interaction.followup.send("")
            except:
                pass
            x=xo(self.opponent,self.interaction)
            await self.origin.edit(content=f"🎲 `{x.fp[0].name}` VS `{x.sp[0].name}`\n\n <@{x.current[0].id}> ,Its yours Turn",embed=None,view=x)
            x.origin = self.origin

    @button(label="Decline",style=discord.ButtonStyle.red)
    async def de(self,interaction:discord.Interaction,button):
        await interaction.response.defer()
        if await self.check(interaction):
            try:
                await interaction.followup.send("")
            except:
                pass
            embed = discord.Embed(title = "Challenge Declined",description=f"{self.opponent.name} dont accept {self.interaction.user.name}'s challenge")
            await self.origin.edit(embed = embed,view=None)

class tictactoe(commands.Cog):
  def __init__(self,bot):
     self.bot = bot
    
  async def check_ban(self,v):
      if self.bot.mango['ban'].find_one({'user_id':str(v)}):
        return True
      else:
        return False
      
  @app_commands.command(name="tictactoe",description="Play tictactoe(XO)")
  @app_commands.describe(opponent="Your opponent")
  async def tictactoe(self,interaction:discord.Interaction,opponent:discord.Member):
    await interaction.response.defer()
    if await self.check_ban(interaction.user.id):
        respound = get_respound(interaction.locale,"baned")
        embed = createembed.baned(interaction,interaction.client,respound)
        d = await interaction.followup.send(embed=embed)
        await asyncio.sleep(5)
        await d.delete()
        return
    embed = discord.Embed(title = "New duel challenge",description=f"<@{opponent.id}> you were challenged by <@{interaction.user.id}> to play `TIC TAC TOE`\n React to button to Accept or Decline the duel")
    view = Accept(opponent,interaction)
    origin = await interaction.followup.send(embed=embed,view=view)
    view.origin = origin


async def setup(bot):
  await bot.add_cog(tictactoe(bot))