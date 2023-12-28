import nextcord as discord
from nextcord.ext import commands
from src.scripts.menu import GalleryMenu
from src.scripts.manager import *
from src.scripts.checks import *
from random import randint

class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.IM = ImageManager(self.bot, CG.DATABASE_PATH, CG.DATABASE_DISCORD_CHANNEL_ID)

    @commands.Cog.listener()
    async def on_ready(self):
        if CG.DATABASE_DISCORD_CHANNEL_ID:
            await self.IM.read_historical_messages()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == CG.DATABASE_DISCORD_CHANNEL_ID and message.author != self.bot.user:
            await self.IM.read_historical_messages()

    @discord.slash_command(name = 'gallery', description = 'All Images at a glance')
    @is_admin()
    async def Gallery(self, interaction: discord.Interaction):
        embed, image = self.IM.get_Image(1)
        await interaction.response.send_message(view = GalleryMenu(interaction.user, self.IM), embed = embed, file = image)

    @discord.slash_command(name = 'image', description = 'View a random picture')
    async def Image(self, interaction: discord.Interaction, image: int = 0):
        if interaction.user.id not in CG.ADMINS.values() or not (0 < image <= self.IM.get_data_size()):
            image = randint(1, self.IM.get_data_size())

        embed, image = self.IM.get_Image(image)
        await interaction.response.send_message(embed = embed, file = image)

    @discord.slash_command(name = 'set', description = 'Sets the channel for uploading the database images')
    @is_owner()
    async def Set(self, interaction: discord.Interaction, channel: discord.TextChannel):
        CG.set_channel(channel)
        await interaction.response.send_message(f'{channel.name} is now the new database channel')


def setup(bot):
    bot.add_cog(Database(bot))