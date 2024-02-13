import nextcord as discord
from nextcord.ext import commands
from src.scripts.checks import *

class ServerManagment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name = 'clean', description = 'Deletes the last x messages')
    @is_admin()
    async def Clean(self, interaction: discord.Interaction, number: int = float('inf'), botonly: bool = False, parameters: str = ''):
        await interaction.response.defer(ephemeral = True)
        
        async for message in interaction.channel.history(limit = None):
            if not number:
                break
            if number and (botonly and message.author == self.bot.user or not botonly) and (parameters == '' or any(word in message.content for word in parameters.split())):
                await message.delete()
                number -= 1

        await interaction.delete_original_message()

def setup(bot):
    bot.add_cog(ServerManagment(bot))