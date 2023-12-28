import nextcord as discord
from nextcord.ext import application_checks
from src.scripts.config import *

CG = Config()

def is_owner():
    def predicate(interaction: discord.Interaction):
        return interaction.user.id in CG.OWNER.values() or interaction.guild.owner.id == interaction.user.id
    return application_checks.check(predicate)


def is_admin():
    def predicate(interaction: discord.Interaction):
        return interaction.user.id in CG.ADMINS.values()
    return application_checks.check(predicate)