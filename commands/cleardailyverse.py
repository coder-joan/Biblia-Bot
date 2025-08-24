import discord

from discord import app_commands
from config.colors import SUCCESS_COLOR, ERROR_COLOR
from services.dailyverse_settings_db import delete_dailyverse_settings, get_dailyverse_settings

@app_commands.command(
    name="cleardailyverse",
    description="Usuwa automatyzację wersetu dnia"
)

async def cleardailyverse(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)

    user_id = interaction.user.id
    guild_id = interaction.guild.id

    settings = get_dailyverse_settings(user_id, guild_id)

    if settings:
        delete_dailyverse_settings(user_id, guild_id)

        embed = discord.Embed(
            title="Usunięto pomyślnie",
            description="Automatyzacja wersetu dnia została usunięta",
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