import discord

from discord import app_commands
from utils.load_json import load_json
from config.paths import TRANSLATIONS
from config.colors import STANDARD_COLOR
from services.user_translation_db import get_user_settings
from services.dailyverse_settings_db import get_dailyverse_settings

@app_commands.command(name="mysettings", description="Wyświetla bieżące ustawienia użytkownika")
async def mysettings(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)

    translations = load_json(TRANSLATIONS)

    user_id = interaction.user.id
    guild_id = interaction.guild.id

    user_data = get_user_settings(user_id)
    dailyverse_data = get_dailyverse_settings(user_id, guild_id)

    translation = user_data[1] if user_data else "-"
    translation = translations.get(translation, translation)

    if dailyverse_data:
        channel_id, hour, timezone = dailyverse_data

        dailyverse_text = (
                f"Automatyzacja wersetu dnia: **włączona**\n"
                f"- Kanał: <#{channel_id}>\n"
                f"- Godzina: `{hour}:00`\n"
                f"- Strefa czasowa: `{timezone}`"
        )
    else:
        dailyverse_text = (
                f"Automatyzacja wersetu dnia: **wyłączona**\n"
                f"- Kanał: -\n"
                f"- Godzina: -\n"
                f"- Strefa czasowa: -"
        )

    embed = discord.Embed(
        title="Twoje ustawienia",
        description=f"{dailyverse_text}\n\nPrzekład Pisma Świętego: `{translation}`",
        color=STANDARD_COLOR
    )

    await interaction.followup.send(embed=embed, ephemeral=True)