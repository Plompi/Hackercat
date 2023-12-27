import nextcord as discord
from nextcord.ext import commands

class ServerManagment(commands.Cog):
    def __init__(self, bot, CG, IM):
        self.bot = bot
        self.CG = CG
        self.IM = IM

    @discord.slash_command(name = 'clean', description = 'Deletes the last x messages')
    async def Clean(self, interaction: discord.Interaction, number: int = float('inf'), botonly: bool = False):
        if interaction.user.id in self.CG.ADMINS.values():
            await interaction.response.send_message('.')
            await interaction.channel.purge(limit = number+1, check = lambda message: not botonly or message.author == self.bot.user)


def setup(bot, CG, IM):
    bot.add_cog(ServerManagment(bot, CG, IM))