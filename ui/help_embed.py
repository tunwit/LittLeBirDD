import discord

class embed:

    def embed(bot,respound,interaction):
        botpro = bot.user.avatar.url
        Homeembed=discord.Embed(title=f"{bot.user.name} | {respound.get('mainmenu')}",description=respound.get('descript'),color=0x53BD40)
        Homeembed.add_field(name=respound.get('invite'),value="[Invite link](https://discord.com/api/oauth2/authorize?client_id=891358646091513927&permissions=8&scope=bot%20applications.commands)")
        Homeembed.set_image(url="https://cdn.discordapp.com/attachments/892983435696685077/946832039569686548/Thnk_2.gif")
        Homeembed.set_footer(text =f"1/6 {respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url)
        #-----------------
        musicembed=discord.Embed(title=f"{bot.user.name} |{respound.get('songcom')}",description=respound.get('descriptsong'),color=0x53BD40)
        musicembed.add_field(name=f"/play <search>",value=respound.get('play'))
        musicembed.add_field(name=f"/pause",value=respound.get('pause'))
        musicembed.add_field(name=f"/resume",value=respound.get('resume'))
        musicembed.add_field(name=f"/skip",value=respound.get('skip'))
        musicembed.add_field(name=f"/loop",value=respound.get('loop'))
        musicembed.add_field(name=f"/filters <type>",value=respound.get('filters'))
        musicembed.add_field(name=f"/ql",value=respound.get('ql'))
        musicembed.add_field(name=f"/remove <number>",value=respound.get('remove'))
        musicembed.add_field(name=f"/dc",value=respound.get('dc'))
        musicembed.set_thumbnail(url=botpro)
        musicembed.set_footer(text =f"2/6 {respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url)
        #-----------------
        crembed=discord.Embed(title=f"{bot.user.name} | {respound.get('crcom')}",description=respound.get('descriptcr'),color=0x53BD40)
        crembed.add_field(name=f"/cr",value=respound.get('cr'))
        crembed.add_field(name=f"/cr_random",value=respound.get('cr_random'))
        crembed.add_field(name=f"/cr_list",value=respound.get('cr_list'))
        crembed.add_field(name=f"/cr_remove <number>",value=respound.get('cr_remove'))
        crembed.add_field(name=f"/cr_clear",value=respound.get('cr_clear'))
        crembed.set_thumbnail(url=botpro)
        crembed.set_footer(text = f"3/6 {respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url)
        #-----------------
        acembed=discord.Embed(title=f"{bot.user.name} | {respound.get('accom')}",description=respound.get('descriptac'),color=0x53BD40)
        acembed.add_field(name=f"/activities",value=respound.get('activities'))
        acembed.add_field(name=f"/gif [search]",value=respound.get('gif'))
        acembed.add_field(name=f"/anime [secret]",value=respound.get('anime'))
        acembed.add_field(name=f"/lyrics <songname>",value=respound.get('lyrics'))
        acembed.set_thumbnail(url=botpro)
        acembed.set_footer(text = f"4/6 {respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url)
        #-----------------
        vsembed=discord.Embed(title=f"{bot.user.name} | {respound.get('vscom')}",description=respound.get('descriptvs'),color=0x53BD40)
        vsembed.add_field(name=f"/play Lplaylist",value=respound.get('Lplaylist'))
        vsembed.add_field(name=f"/create_playlist",value=respound.get('create_playlist'))
        vsembed.add_field(name=f"/addplaylist <search>",value=respound.get('addplaylist'))
        vsembed.add_field(name=f"/remove_playlist <number>",value=respound.get('remove_playlist'))
        vsembed.add_field(name=f"/clear_playlist",value=respound.get('clear_playlist'))
        vsembed.add_field(name=f"/ql_playlist",value=respound.get('ql_playlist'))
        vsembed.set_thumbnail(url=botpro)
        vsembed.set_footer(text = f"5/6 {respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url)
        #-----------------
        cfembed=discord.Embed(title=f"{bot.user.name} | {respound.get('cfcom')}",description=respound.get('descriptcf'),color=0x53BD40)
        cfembed.add_field(name=f"/toggle_lv",value=respound.get('toggle_lv'))
        cfembed.add_field(name=f"/lv",value=respound.get('lv'))
        cfembed.add_field(name=f"/setup_stats",value=respound.get('setup_stats'),inline = False)
        cfembed.add_field(name=f"/reset_stats",value=respound.get('reset_stats'))
        cfembed.add_field(name=f"/welcomemessage",value=respound.get('welcomemessage'))
        cfembed.set_thumbnail(url=botpro)
        cfembed.set_footer(text = f"6/6 {respound.get('requester').format(user=interaction.user.name)}", icon_url=interaction.user.avatar.url)
        return [Homeembed,musicembed,crembed,acembed,vsembed,cfembed]