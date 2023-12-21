import nextcord as discord

class Menu(discord.ui.View):
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