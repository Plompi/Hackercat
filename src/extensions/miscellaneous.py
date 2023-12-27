import nextcord as discord
from nextcord.ext import commands
from random import choice

class Miscellaneous(commands.Cog):
    def __init__(self, bot, CG, IM):
        self.bot = bot
        self.CG = CG
        self.IM = IM

    @discord.slash_command(name = 'coin', description = 'Flip a coin and see if you win')
    async def Coin(self, interaction: discord.Interaction, site: str = discord.SlashOption(name = 'site', choices = ['head', 'tails'])):
        if site == choice(['head', 'tails']):
            await interaction.response.send_message('you won 👑')
        else:
            await interaction.response.send_message('you lost :(')


def setup(bot, CG, IM):
    bot.add_cog(Miscellaneous(bot, CG, IM))