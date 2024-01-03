from discord.ui import View, Button , button
import discord

class buttin(View):
  def __init__(self,total_pages:list,timeout:float,interaction:discord.Interaction):
    super().__init__(timeout=timeout)
    self.current_page = 0
    self.interaction = interaction
    self.total_pages = total_pages
    self.lenght = len(self.total_pages)-1
    self.children[0].disabled = True
    self.children[1].disabled = True
    self.children[-1].disabled = True if self.lenght == 0 else False
    self.children[-2].disabled = True if self.lenght == 0 else False
  
  async def update(self,page:int):
    self.current_page = page
    if page == 0 and not self.lenght == 0:
      self.children[0].disabled = True
      self.children[1].disabled = True
      self.children[-1].disabled = False
      self.children[-2].disabled = False
    elif page == 0 and self.lenght == 0:
      self.children[0].disabled = False
      self.children[1].disabled = False
      self.children[-1].disabled = False
      self.children[-2].disabled = False     
    elif page == self.lenght:
      self.children[0].disabled = False
      self.children[1].disabled = False
      self.children[-1].disabled = True
      self.children[-2].disabled = True
    else:
      for i in self.children:
        i.disabled = False

  async def on_timeout(self):
    await self.interaction.delete_original_response()
    self.stop()
    
  async def respounded(self,page:int,interaction:discord.Interaction):
    await self.update(page)
    await interaction.response.edit_message(embed=self.total_pages[page],view=self)
    self.interaction = interaction

  @button(emoji="<a:11:989120441325068308>",style=discord.ButtonStyle.blurple)
  async def first(self,interaction:discord.Interaction,button):
    await self.respounded(0,interaction)

  @button(emoji="<a:12:989120435364962334>",style=discord.ButtonStyle.green)
  async def previous(self,interaction:discord.Interaction,button):
    await self.respounded(self.current_page-1,interaction)

  @button(emoji="<a:8_:989120444701491210>",style=discord.ButtonStyle.red)
  async def delete(self,interaction:discord.Interaction,button):
    await self.interaction.delete_original_response()
    self.stop()

  @button(emoji="<a:13:989120437688627200>",style=discord.ButtonStyle.green)
  async def next(self,interaction:discord.Interaction,button):
    await self.respounded(self.current_page+1,interaction)

  @button(emoji="<a:10:989120439655739432>",style=discord.ButtonStyle.blurple)
  async def last(self,interaction:discord.Interaction,button):
    await self.respounded(self.lenght,interaction)
