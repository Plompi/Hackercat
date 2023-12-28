import nextcord as discord
from nextcord.ext import commands
from src.scripts.checks import *

class ServerManagment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name = 'clean', description = 'Deletes the last x messages')
    @is_admin()
    async def Clean(self, interaction: discord.Interaction, number: int = float('inf'), botonly: bool = False):
        await interaction.response.send_message('.')
        await interaction.channel.purge(limit = number+1, check = lambda message: not botonly or message.author == self.bot.user)


def setup(bot):
    bot.add_cog(ServerManagment(bot))