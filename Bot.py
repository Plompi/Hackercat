import nextcord as discord
from nextcord import Member, SlashOption
from nextcord.ext import commands
from random import randint, choice
import os,sys
from PIL import Image as PilImage, ImageDraw
from io import BytesIO
from src.scripts.config import *
from src.scripts.manager import *
from src.scripts.menu import *

bot = commands.Bot(command_prefix = '!', intents = discord.Intents.all(), case_insensitive = True)
CG = Config()
IM = ImageManager(bot, CG.DATABASE_PATH, CG.DATABASE_DISCORD_CHANNEL_ID)

def load_extensions():
    for ext in CG.EXTENSIONS:
        bot.load_extension(ext, extras={'CG' : CG})

@bot.event
async def on_ready():
    loadPersistentMenus(bot, CG)
    if CG.DATABASE_DISCORD_CHANNEL_ID:
        await IM.read_historical_messages()


@bot.event
async def on_message(message):
    if message.channel.id == CG.DATABASE_DISCORD_CHANNEL_ID and message.author != bot.user:
        await IM.read_historical_messages()


@bot.slash_command(name = 'extensions', description = 'Manage the Bot Extensions')
async def Extensions(interaction: discord.Interaction):
    await interaction.response.send_message(view = ExtensionMenu(CG), content = 'Select an Extension to enable/disable')


@bot.slash_command(name = 'gallery', description = 'All Images at a glance')
async def Gallery(interaction: discord.Interaction):
    if interaction.user.id in CG.ADMINS.values():
        embed, image = IM.get_Image(1)
        await interaction.response.send_message(view = GalleryMenu(interaction.user, IM), embed = embed, file = image)
    else:
        await interaction.response.send_message('You dont have the Admin Permission')


@bot.slash_command(name = 'image', description = 'View a random picture')
async def Image(interaction: discord.Interaction, image:int = 0):
    if interaction.user.id not in CG.ADMINS.values() or not (0 < image <= IM.get_data_size()):
        image = randint(1, IM.get_data_size())

    embed, image = IM.get_Image(image)
    await interaction.response.send_message(embed = embed, file = image)


@bot.slash_command(name = 'bonk', description = 'Bonk someone right over the head')
async def Bonk(interaction: discord.Interaction, member: Member = None):
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


@bot.slash_command(name = 'poop', description = 'Someone has to clean the toilet')
async def Poop(interaction: discord.Interaction, member: Member = None):
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


@bot.slash_command(name = 'clean', description = 'Deletes the last x messages')
async def Clean(interaction: discord.Interaction, number: int = float('inf'), botonly: bool = False):
    await interaction.response.send_message('.')
    await interaction.channel.purge(limit = number+1, check = lambda message: not botonly or message.author == bot.user)


@bot.slash_command(name = 'set', description = 'Sets the channel for uploading the database images')
async def Set(interaction: discord.Interaction, channel: discord.TextChannel):
    if interaction.user.id in CG.OWNER.values():
        CG.set_channel(channel)
        await interaction.response.send_message(f'{channel.name} is now the new database channel')
    else:
        await interaction.response.send_message('You dont have the Owner Permission')


@bot.slash_command(name = 'update', description = 'Update the config.json manually')
async def Update(interaction: discord.Interaction):
    if interaction.user.id in CG.OWNER.values():
        CG.load_config()
        await interaction.response.send_message('The config has been reloaded')
    else:
        await interaction.response.send_message('You dont have the Owner Permission')


@bot.slash_command(name = 'owner', description = 'Sets the bot owner')
async def Owner(interaction: discord.Interaction, user: discord.User):
    if interaction.user.id in CG.OWNER.values() or interaction.user == bot.guilds[0].owner:
        CG.set_owner(user)
        await interaction.response.send_message(f'{user} is now the Hackercat owner')
    else:
        await interaction.response.send_message('You dont have the Owner Permission')


@bot.slash_command(name = 'op', description = 'Give a user admin rights for this bot')
async def Op(interaction: discord.Interaction, user: discord.User):
    if interaction.user.id in CG.OWNER.values():
        CG.add_admin(user)
        await interaction.response.send_message(f'{user} is now a Hackercat')
    else:
        await interaction.response.send_message('You dont have the Owner Permission')

@bot.slash_command(name = 'deop', description = 'Take away a users admin rights for this bot')
async def Deop(interaction: discord.Interaction, user: discord.User):
    if interaction.user.id in CG.OWNER.values():
        CG.del_admin(user)
        await interaction.response.send_message(f'{user} is no longer a Hackercat')
    else:
        await interaction.response.send_message('You dont have the Owner Permission')


@bot.slash_command(name = 'coin', description = 'Flip a coin and see if you win')
async def Coin(interaction: discord.Interaction, site: str = SlashOption(name = 'site', choices = ['head', 'tails'])):
    if site == choice(['head', 'tails']):
        await interaction.response.send_message('you won 👑')
    else:
        await interaction.response.send_message('you lost :(')

load_extensions()
bot.run(CG.TOKEN)
