import discord

from discord import app_commands
from utils.load_json import load_json
from config.paths import TRANSLATIONS
from config.colors import ERROR_COLOR, SUCCESS_COLOR
from services.user_settings_db import set_user_translation

async def translation_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> list[app_commands.Choice[str]]:
    bible_translations = load_json(TRANSLATIONS)
    return [
        app_commands.Choice(name=full_name, value=abbreviation)
        for abbreviation, full_name in bible_translations.items()
        if current.lower() in full_name.lower()
    ][:25]

@app_commands.command(name="setversion", description="Ustawia domyślny przekład Pisma Świętego")
@app_commands.describe(translation="Wybierz przekład Pisma Świętego")
@app_commands.autocomplete(translation=translation_autocomplete)
async def setversion(interaction: discord.Interaction, translation: str):
    await interaction.response.defer(ephemeral=True)

    bible_translations = load_json(TRANSLATIONS)

    if translation not in bible_translations.keys():
        error_embed = discord.Embed(
            title="Błąd",
            description=(
                "Podano błędny przekład Pisma Świętego. Użyj autouzupełniania lub sprawdź "
                "dostępne skróty przekładów w komendzie `/versions`"
            ),
            color=ERROR_COLOR
        )
        await interaction.followup.send(embed=error_embed, ephemeral=True)
        return

    set_user_translation(interaction.user.id, translation)
    translation = bible_translations.get(translation, translation)

    embed = discord.Embed(
        title="Ustawiono pomyślnie",
        description=f"Twoim domyślnym przekładem Pisma Świętego jest: `{translation}`",
        color=SUCCESS_COLOR
    )
    await interaction.followup.send(embed=embed, ephemeral=True)