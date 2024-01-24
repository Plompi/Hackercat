import nextcord as discord
from random import shuffle

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
    async def firstImage(self, _, interaction):
        await self.handle_button_click(interaction, new_value = 1)

    @discord.ui.button(label = '❮', style = discord.ButtonStyle.grey)
    async def prevImage(self, _, interaction):
        await self.handle_button_click(interaction, new_value = max(1,self.image - 1))

    @discord.ui.button(label= '❯' , style = discord.ButtonStyle.grey)
    async def nextImage(self, _, interaction):
        await self.handle_button_click(interaction, new_value = min(self.IM.get_data_size(),self.image + 1))

    @discord.ui.button(label = '❯❯', style = discord.ButtonStyle.grey)
    async def lastImage(self, _, interaction):
        await self.handle_button_click(interaction, new_value = self.IM.get_data_size())

    @discord.ui.button(label = '🗑️', style = discord.ButtonStyle.red)
    async def delImage(self, _, interaction):
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
    async def addRole(self, _, interaction):
        if self.limit:
            if len(self.role.members) < self.limit and interaction.user not in self.role.members:
                await interaction.user.add_roles(self.role)
                await interaction.message.edit(content = f'{len(self.role.members)}/{self.limit} member(s) participate')
        else:
            if interaction.user not in self.role.members:
                await interaction.user.add_roles(self.role)
                await interaction.message.edit(content = f'{len(self.role.members)} member(s) participate')
    
    @discord.ui.button(label = 'leave', style = discord.ButtonStyle.red, custom_id='leaveButton')
    async def delRole(self, _, interaction):
        if interaction.user in self.role.members:    
            await interaction.user.remove_roles(self.role)
            if self.limit:
                await interaction.message.edit(content = f'{len(self.role.members)}/{self.limit} member(s) participate')
            else:
                await interaction.message.edit(content = f'{len(self.role.members)} member(s) participate')

    @discord.ui.button(label = '🎁', style = discord.ButtonStyle.grey, custom_id='startButton')
    async def start(self, _, interaction):
        if interaction.user.id == self.author:
            x = self.role.members
            shuffle(x)

            for i in range(len(x)-1,-1,-1):
                await x[i].send(f'You got {str(x[i-1])}')

            await interaction.message.edit(content = 'let the gift-giving begin', view = None)
            await self.role.delete()
            self.stop()


class ExtensionMenu(discord.ui.View):
    def __init__(self, CG, author, bot):
        super().__init__(timeout = 600)
        self.author = author
        self.add_item(ExtensionSelectMenu(CG, self, bot))

class ExtensionSelectMenu(discord.ui.Select):
    def __init__(self, CG, view, bot):
        self.Selectview = view
        self.CG = CG
        self.bot = bot
        options = [discord.SelectOption(label='save Changes', value='Restart', emoji='🔄')] + [discord.SelectOption(label=ext[15:], emoji='✅' if ext in self.CG.EXTENSIONS else '❌') for ext in self.CG.all_extensions()]
        super().__init__(placeholder = 'Select Extension', min_values = 1, max_values = 1, options = options)

    async def callback(self, interaction):
        if interaction.user == self.Selectview.author:
            if self.values[0] == 'Restart':
                #Works Currently but not optimal, should use sync_application_commands with GUILD_ID
                await interaction.message.delete()
                await self.bot.sync_application_commands() 
            else:
                # await interaction.response.defer()
                # cog = self.bot.get_cog(self.values[0].capitalize()) # currently doesnt Work with ServerManagment & ProfileMorph because of capitalization
                extension = f'src.extensions.{self.values[0]}'
                self.CG.toggle_extension(extension)
                if extension in self.CG.EXTENSIONS:
                    self.bot.load_extension(extension)
                    # cog = self.bot.get_cog(self.values[0].capitalize())
                else:
                    self.bot.unload_extension(extension)

                
                
                # cog_commands = cog.get_commands()
                # await self.bot.sync_application_commands(data=cog_commands)

                await interaction.message.edit(view = ExtensionMenu(self.CG, self.Selectview.author, self.bot))
                self.Selectview.stop()
    