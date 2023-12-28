import nextcord as discord
from nextcord.ext import commands
from random import choice
from src.scripts.checks import *

class Miscellaneous(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name = 'coin', description = 'Flip a coin and see if you win')
    async def Coin(self, interaction: discord.Interaction, site: str = discord.SlashOption(name = 'site', choices = ['head', 'tails'])):
        if site == choice(['head', 'tails']):
            await interaction.response.send_message('you won 👑')
        else:
            await interaction.response.send_message('you lost :(')


def setup(bot):
    bot.add_cog(Miscellaneous(bot))