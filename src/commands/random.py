import discord

from discord import app_commands
from random import randint
from utils.load_json import load_json
from utils.italic_font import italic_font
from utils.autocomplete import translation_autocomplete
from config.colors import STANDARD_COLOR, ERROR_COLOR
from config.paths import POLISH_BOOK_NAMES, TRANSLATIONS
from services.user_translation_db import get_user_settings
from services.bibles_db import get_bible_connection, get_random_verse, get_following_verses

@app_commands.command(name="random", description="Wyświetla losowy werset")
@app_commands.describe(translation="Wybierz przekład Pisma Świętego")
@app_commands.autocomplete(translation=translation_autocomplete)
async def random(interaction: discord.Interaction, translation: str = None):
    await interaction.response.defer()

    user_id = interaction.user.id
    user_data = get_user_settings(user_id)

    translations = load_json(TRANSLATIONS)

    if translation:
        chosen_translation = translation
    elif user_data:
        chosen_translation = user_data[1]
    else:
        embed = discord.Embed(
            title="Ustaw domyślny przekład Pisma Świętego",
            description=(
                'Zanim rozpoczniesz wyszukiwanie fragmentów w Biblii, '
                'ustaw domyślny przekład Pisma Świętego za pomocą komendy `/setversion`'
            ),
            color=STANDARD_COLOR
        )
        await interaction.followup.send(embed=embed)
        return
    
    if chosen_translation not in translations:
        error_embed = discord.Embed(
            title="Błąd",
            description=(
                "Podano błędny przekład Pisma Świętego. Użyj autouzupełniania lub sprawdź "
                "dostępne skróty przekładów w komendzie `/versions`"
            ),
            color=ERROR_COLOR
        )
        await interaction.followup.send(embed=error_embed)
        return

    conn = get_bible_connection()
    cursor = conn.cursor()

    row = get_random_verse(cursor, chosen_translation)

    if not row:
        error_embed = discord.Embed(
            title="Błąd",
            description="Nie znaleziono wersetów dla tego przekładu",
            color=ERROR_COLOR
        )
        await interaction.followup.send(embed=error_embed)
        return

    book_name, book_number, chapter, start_verse, text = row
    number_of_verses = randint(1, 10)

    verses = get_following_verses(cursor, chosen_translation, book_number, chapter, start_verse, number_of_verses)

    conn.close()

    polish_book_names = load_json(POLISH_BOOK_NAMES)

    polish_book_name = polish_book_names.get(book_name, book_name)
    first_verse, last_verse = verses[0][0], verses[-1][0]

    verses_text = ""
    
    for verse_number, verse_text in verses:
        formatted_text = italic_font(verse_text).replace("\n", " ").replace("  ", " ").strip()
        verses_text += f"**({verse_number})** {formatted_text} "

    if first_verse == last_verse:
        title = f"{polish_book_name} {chapter}:{first_verse}"
    else:
        title = f"{polish_book_name} {chapter}:{first_verse}-{last_verse}"

    embed = discord.Embed(
        title=title,
        description=verses_text[:4093],
        color=STANDARD_COLOR
    )
    embed.set_footer(text=translations.get(chosen_translation, chosen_translation))
    await interaction.followup.send(embed=embed)
