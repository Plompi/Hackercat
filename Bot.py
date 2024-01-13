import nextcord as discord
from nextcord.ext import commands
from src.scripts.menu import ExtensionMenu
from src.scripts.checks import *

bot = commands.Bot(intents = discord.Intents.all())

@bot.event
async def on_application_command_error(interaction, error):
    if isinstance(error, discord.errors.ApplicationCheckFailure):
        await interaction.response.send_message("You dont have Permission", ephemeral = True)


@bot.slash_command(name = 'extensions', description = 'Manage the Bot Extensions')
@is_owner()
async def Extensions(interaction: discord.Interaction):
    await interaction.response.send_message(view = ExtensionMenu(CG, interaction.user), content = 'Select an Extension to enable/disable')


@bot.slash_command(name = 'update', description = 'Update the config.json manually')
@is_owner()
async def Update(interaction: discord.Interaction):
    CG.load_config()
    await interaction.response.send_message('The config has been reloaded')


@bot.user_command(name = 'own')
@is_owner()
async def Own(interaction: discord.Interaction, member: discord.Member):
    CG.add_owner(member)
    await interaction.response.send_message(f'{member} is now a Hackercat owner')

@bot.user_command(name = 'deown')
@is_owner()
async def Deown(interaction: discord.Interaction, member: discord.Member):
    CG.del_owner(member)
    await interaction.response.send_message(f'{member} is no longer a Hackercat owner')

@bot.user_command(name = 'op')
@is_owner()
async def Op(interaction: discord.Interaction, member: discord.Member):
    CG.add_admin(member)
    await interaction.response.send_message(f'{member} is now a Hackercat')

@bot.user_command(name = 'deop')
@is_owner()
async def Deop(interaction: discord.Interaction, member: discord.Member):
    CG.del_admin(member)
    await interaction.response.send_message(f'{member} is no longer a Hackercat')
    


if __name__ == '__main__':
    for ext in CG.EXTENSIONS:
        bot.load_extension(ext)
    bot.run(CG.TOKEN)