import discord

from discord import app_commands
from config.colors import SUCCESS_COLOR, ERROR_COLOR
from services.user_settings_db import get_user_settings, remove_user

@app_commands.command(name="removeuserdata", description="Usuwa dane użytkownika z bazy danych")
async def removeuserdata(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)

    user_id = interaction.user.id
    user_data = get_user_settings(user_id)

    if user_data:
        remove_user(user_id)

        embed = discord.Embed(
            title="Usunięto pomyślnie",
            description=("Twoje dane zostały usunięte z bazy danych"),
            color=SUCCESS_COLOR
        )
        await interaction.followup.send(embed=embed, ephemeral=True)
    else:
        error_embed = discord.Embed(
            title="Brak danych",
            description="Nie znaleziono twoich danych w bazie danych",
            color=ERROR_COLOR
        )
        await interaction.followup.send(embed=error_embed, ephemeral=True)