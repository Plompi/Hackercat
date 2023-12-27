import nextcord as discord
from nextcord.ext import commands
from src.scripts.config import *
from src.scripts.manager import *
from src.scripts.menu import *

bot = commands.Bot(command_prefix = '!', intents = discord.Intents.all(), case_insensitive = True)
CG = Config()
IM = ImageManager(bot, CG.DATABASE_PATH, CG.DATABASE_DISCORD_CHANNEL_ID)

def load_extensions():
    for ext in CG.EXTENSIONS:
        bot.load_extension(ext, extras={'CG' : CG, 'IM' : IM})

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
    if interaction.user.id in CG.OWNER.values():
        await interaction.response.send_message(view = ExtensionMenu(CG), content = 'Select an Extension to enable/disable')


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


load_extensions()
bot.run(CG.TOKEN)
