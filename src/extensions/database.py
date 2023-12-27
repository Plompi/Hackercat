import nextcord as discord
from nextcord.ext import commands
from src.scripts.menu import GalleryMenu
from random import randint

class Database(commands.Cog):
    def __init__(self, bot, CG, IM):
        self.bot = bot
        self.CG = CG
        self.IM = IM

    @discord.slash_command(name = 'gallery', description = 'All Images at a glance')
    async def Gallery(self, interaction: discord.Interaction):
        if interaction.user.id in self.CG.ADMINS.values():
            embed, image = self.IM.get_Image(1)
            await interaction.response.send_message(view = GalleryMenu(interaction.user, self.IM), embed = embed, file = image)
        else:
            await interaction.response.send_message('You dont have the Admin Permission')


    @discord.slash_command(name = 'image', description = 'View a random picture')
    async def Image(self, interaction: discord.Interaction, image:int = 0):
        if interaction.user.id not in self.CG.ADMINS.values() or not (0 < image <= self.IM.get_data_size()):
            image = randint(1, self.IM.get_data_size())

        embed, image = self.IM.get_Image(image)
        await interaction.response.send_message(embed = embed, file = image)


def setup(bot, CG, IM):
    bot.add_cog(Database(bot, CG, IM))