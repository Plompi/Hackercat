import nextcord as discord
from nextcord.ext import commands
from src.scripts.menu import SecretSantaMenu

class Christmas(commands.Cog):
    def __init__(self, bot, CG):
        self.bot = bot
        self.CG = CG

    @discord.slash_command(name = 'secretsanta', description = 'Start a Secret Santa event')
    async def SecretSanta(self, interaction : discord.Interaction, limit: int = 0):
        role = discord.utils.get(interaction.guild.roles, name = 'Elf')
        if not role:
            role = await interaction.guild.create_role(name = 'Elf', color = discord.Color.from_rgb(40, 190, 60))

        view = SecretSantaMenu(role, limit, interaction.user.id)
        content = f'{len(role.members)}{f'/{limit}' if limit else ''} member(s) participate'
        self.CG.set_menu('secretsanta', str(role.guild), limit, interaction.user.id)
        await interaction.response.send_message(view = view, content = content)


def setup(bot, CG):
    bot.add_cog(Christmas(bot, CG))