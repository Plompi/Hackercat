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
        super().__init__()
        self.role = role
        self.limit = limit
        self.author = author

    @discord.ui.button(label = '🎁', style = discord.ButtonStyle.grey)
    async def addRole(self, button, interaction):
        if len(self.role.members) < self.limit and interaction.user not in self.role.members:
            await interaction.user.add_roles(self.role)
    
    @discord.ui.button(label = '❌', style = discord.ButtonStyle.grey)
    async def delRole(self, button, interaction):
        if interaction.user in self.role.members:
            await interaction.user.remove_roles(self.role)

    @discord.ui.button(label = '🏁', style = discord.ButtonStyle.grey)
    async def start(self, button, interaction):
        if interaction.user == self.author:
            x = self.role.members
            shuffle(x)

            for i in range(len(x)-1,-1,-1):
                await x[i].send(f"You got {str(x[i-1])}")

            await interaction.message.edit(content = "let the gift-giving begin", view = None)
            await self.role.delete()
            self.stop()
