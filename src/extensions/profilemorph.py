import nextcord as discord
from nextcord.ext import commands
from PIL import Image as PilImage, ImageDraw
from src.scripts.checks import *
from io import BytesIO
import os

class ProfileMorph(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name = 'bonk', description = 'Bonk someone right over the head')
    async def Bonk(self, interaction: discord.Interaction, member: discord.Member = None):
        if not member:
            member = interaction.user

        result_bytesio = BytesIO()
        Profilepic = PilImage.open(BytesIO(await member.avatar.read())).resize((200, 200))
        result = PilImage.open(os.path.join(CG.IMAGE_PATH,'bonk.jpg')).copy()
        result.paste(Profilepic, (480, 165))
        result.save(result_bytesio, format = 'PNG')
        result_bytesio.seek(0)
        await interaction.response.send_message(file = discord.File(result_bytesio, filename = 'result.png'))
        result_bytesio.close()

    @discord.slash_command(name = 'poop', description = 'Someone has to clean the toilet')
    async def Poop(self, interaction: discord.Interaction, member: discord.Member = None):
        if not member:
            member = interaction.user

        result_bytesio = BytesIO()
        Profilepic = PilImage.open(BytesIO(await member.avatar.read())).resize((390, 390))
        
        mask = PilImage.new('L', Profilepic.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 390, 390), fill = 255)
        temp = PilImage.new('RGBA', Profilepic.size, (255, 255, 255, 0))
        temp.paste(Profilepic.convert('RGBA'), mask = mask)

        result = PilImage.open(os.path.join(CG.IMAGE_PATH,'toilet.png')).copy()
        result.paste(temp, (910, 340), temp)
        result.save(result_bytesio, format = 'PNG')
        result_bytesio.seek(0)
        await interaction.response.send_message(file = discord.File(result_bytesio, filename = 'result.png'))
        result_bytesio.close()


def setup(bot):
    bot.add_cog(ProfileMorph(bot))