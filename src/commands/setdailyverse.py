import discord, pytz

from discord import app_commands
from utils.autocomplete import timezone_autocomplete
from services.user_translation_db import get_user_settings
from services.dailyverse_settings_db import set_dailyverse_settings
from config.colors import SUCCESS_COLOR, ERROR_COLOR, STANDARD_COLOR

@app_commands.command(name="setdailyverse", description="Ustawia automatyzację wersetu dnia")
@app_commands.describe(
    channel="Wybierz kanał",
    hour="Wprowadź godzinę (0–23)",
    timezone="Wybierz strefę czasową"
)
@app_commands.autocomplete(timezone=timezone_autocomplete)

async def setdailyverse(
    interaction: discord.Interaction,
    channel: discord.TextChannel,
    hour: int,
    timezone: str
):
    await interaction.response.defer(ephemeral=True)

    user_data = get_user_settings(interaction.user.id)

    if not user_data or not user_data[1]:  
        error_embed = discord.Embed(
            title="Ustaw domyślny przekład Pisma Świętego",
            description=(
                'Zanim rozpoczniesz wyszukiwanie fragmentów w Biblii, '
                'ustaw domyślny przekład Pisma Świętego za pomocą komendy `/setversion`'
            ),
            color=STANDARD_COLOR
        )
        await interaction.followup.send(embed=error_embed, ephemeral=True)
        return

    if hour < 0 or hour > 23:
        error_embed = discord.Embed(
            title="Błąd",
            description="Godzina musi mieścić się w przedziale od 0 do 23",
            color=ERROR_COLOR
        )
        await interaction.followup.send(embed=error_embed, ephemeral=True)
        return
    
    if timezone not in pytz.all_timezones:
        error_embed = discord.Embed(
            title="Błąd",
            description="Podano nieprawidłową strefę czasową. Proszę skorzystać z autouzupełniania",
            color=ERROR_COLOR
        )
        await interaction.followup.send(embed=error_embed, ephemeral=True)
        return
        
    set_dailyverse_settings(interaction.user.id, interaction.guild.id, channel.id, hour, timezone)

    embed = discord.Embed(
        title="Włączono automatyzację wersetu dnia",
        description=(
            f"Kanał: {channel.mention}\n"
            f"Godzina: `{hour}:00`\n"
            f"Strefa czasowa: `{timezone}`"
        ),
        color=SUCCESS_COLOR
    )
    await interaction.followup.send(embed=embed, ephemeral=True)