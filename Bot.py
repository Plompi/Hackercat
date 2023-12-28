import nextcord as discord
from nextcord.ext import commands
from src.scripts.config import *
from src.scripts.manager import *
from src.scripts.menu import *
from src.scripts.checks import *

bot = commands.Bot(command_prefix = '!', intents = discord.Intents.all(), case_insensitive = True)
IM = ImageManager(bot, CG.DATABASE_PATH, CG.DATABASE_DISCORD_CHANNEL_ID)

def load_extensions():
    for ext in CG.EXTENSIONS:
        bot.load_extension(ext)


@bot.event
async def on_ready():
    loadPersistentMenus(bot, CG)


@bot.event
async def on_application_command_error(interaction, error):
    if isinstance(error, discord.errors.ApplicationCheckFailure):
        await interaction.response.send_message("You dont have Permission")


@bot.slash_command(name = 'extensions', description = 'Manage the Bot Extensions')
@is_owner()
async def Extensions(interaction: discord.Interaction):
    await interaction.response.send_message(view = ExtensionMenu(CG, interaction.user), content = 'Select an Extension to enable/disable')


@bot.slash_command(name = 'update', description = 'Update the config.json manually')
@is_owner()
async def Update(interaction: discord.Interaction):
    CG.load_config()
    await interaction.response.send_message('The config has been reloaded')


@bot.slash_command(name = 'owner', description = 'Manage bot owners')
@is_owner()
async def Owner(interaction: discord.Interaction, user: discord.User, option: str = discord.SlashOption(name = 'option', choices = ['add', 'remove'])):
    if option == 'add':
        CG.add_owner(user)
        await interaction.response.send_message(f'{user} is now a Hackercat owner')
    else:
        CG.del_owner(user)
        await interaction.response.send_message(f'{user} is no longer a Hackercat owner')


@bot.slash_command(name = 'admin', description = 'Manage bot admins')
@is_owner()
async def Admin(interaction: discord.Interaction, user: discord.User, option: str = discord.SlashOption(name = 'option', choices = ['add', 'remove'])):
    if option == 'add':
        CG.add_admin(user)
        await interaction.response.send_message(f'{user} is now a Hackercat')
    else:
        CG.del_admin(user)
        await interaction.response.send_message(f'{user} is no longer a Hackercat')


if __name__ == '__main__':
    load_extensions()
    bot.run(CG.TOKEN)