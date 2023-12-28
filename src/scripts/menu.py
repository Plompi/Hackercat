import nextcord as discord
from random import shuffle
import os, sys

def loadPersistentMenus(bot, CG):
    guild = discord.utils.get(bot.guilds, name=CG.MENU['secretsanta'][0])
    role = discord.utils.get(guild.roles, name='Elf')
    bot.add_view(SecretSantaMenu(role,CG.MENU['secretsanta'][1],CG.MENU['secretsanta'][2]))

class GalleryMenu(discord.ui.View):
    def __init__(self, author, ImageManager):
        super().__init__()
        self.image = 1
        self.author = author
        self.IM = ImageManager

    async def update_message(self, interaction):
        embed, image = self.IM.get_Image(self.image)
        await interaction.response.edit_message(embed = embed, file = image)

    async def handle_button_click(self, interaction, new_value = None, deletion = False):
        if new_value:
            if new_value == self.image:
                return
            self.image = new_value
        if deletion:
            self.IM.del_Image(self.image)
            self.image = max(1,min(self.IM.get_data_size(), self.image))
        await self.update_message(interaction)

    @discord.ui.button(label = '❮❮', style = discord.ButtonStyle.grey)
    async def firstImage(self, button, interaction):
        await self.handle_button_click(interaction, new_value = 1)

    @discord.ui.button(label = '❮', style = discord.ButtonStyle.grey)
    async def prevImage(self, button, interaction):
        await self.handle_button_click(interaction, new_value = max(1,self.image - 1))

    @discord.ui.button(label= '❯' , style = discord.ButtonStyle.grey)
    async def nextImage(self, button, interaction):
        await self.handle_button_click(interaction, new_value = min(self.IM.get_data_size(),self.image + 1))

    @discord.ui.button(label = '❯❯', style = discord.ButtonStyle.grey)
    async def lastImage(self, button, interaction):
        await self.handle_button_click(interaction, new_value = self.IM.get_data_size())

    @discord.ui.button(label = '🗑️', style = discord.ButtonStyle.red)
    async def delImage(self, button, interaction):
        await self.handle_button_click(interaction, deletion = True)

    async def interaction_check(self, interaction):
        return interaction.user.id == self.author.id  

class SecretSantaMenu(discord.ui.View):
    def __init__(self, role, limit, author):
        super().__init__(timeout=None)
        self.role = role
        self.limit = limit
        self.author = author

    @discord.ui.button(label = 'join', style = discord.ButtonStyle.green, custom_id='joinButton')
    async def addRole(self, button, interaction):
        if self.limit:
            if len(self.role.members) < self.limit and interaction.user not in self.role.members:
                await interaction.user.add_roles(self.role)
                await interaction.message.edit(content = f'{len(self.role.members)}/{self.limit} member(s) participate')
        else:
            if interaction.user not in self.role.members:
                await interaction.user.add_roles(self.role)
                await interaction.message.edit(content = f'{len(self.role.members)} member(s) participate')
    
    @discord.ui.button(label = 'leave', style = discord.ButtonStyle.red, custom_id='leaveButton')
    async def delRole(self, button, interaction):
        if interaction.user in self.role.members:    
            await interaction.user.remove_roles(self.role)
            if self.limit:
                await interaction.message.edit(content = f'{len(self.role.members)}/{self.limit} member(s) participate')
            else:
                await interaction.message.edit(content = f'{len(self.role.members)} member(s) participate')

    @discord.ui.button(label = '🎁', style = discord.ButtonStyle.grey, custom_id='startButton')
    async def start(self, button, interaction):
        if interaction.user.id == self.author:
            x = self.role.members
            shuffle(x)

            for i in range(len(x)-1,-1,-1):
                await x[i].send(f'You got {str(x[i-1])}')

            await interaction.message.edit(content = 'let the gift-giving begin', view = None)
            await self.role.delete()
            self.stop()


class ExtensionMenu(discord.ui.View):
    def __init__(self, CG, author):
        super().__init__(timeout = 600)
        self.author = author
        self.add_item(ExtensionSelectMenu(CG, self))

class ExtensionSelectMenu(discord.ui.Select):
    def __init__(self, CG, view):
        self.Selectview = view
        self.CG = CG
        options = [discord.SelectOption(label='Restart Bot to apply Changes', value='Restart', emoji='🔄')] + [discord.SelectOption(label=ext[15:], emoji='✅' if ext in self.CG.EXTENSIONS else '❌') for ext in self.CG.all_extensions()]
        super().__init__(placeholder = 'Select Extension', min_values = 1, max_values = 1, options = options)

    async def callback(self, interaction):
        if interaction.user == self.Selectview.author:
            if self.values[0] == 'Restart':
                await interaction.message.delete()
                path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'Bot.py')
                os.execl(sys.executable, sys.executable, path)
            else:
                self.CG.toggle_extension(f'src.extensions.{self.values[0]}')
                await interaction.message.edit(view = ExtensionMenu(self.CG, self.Selectview.author))
                self.Selectview.stop()
    