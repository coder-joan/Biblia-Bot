import discord, re

from discord import app_commands
from utils.load_json import load_json
from utils.italic_font import italic_font
from utils.paginator_view import PaginatorView
from utils.autocomplete import translation_autocomplete
from services.user_translation_db import get_user_settings
from services.bibles_db import search_verses, count_verses
from config.colors import STANDARD_COLOR, ERROR_COLOR
from config.paths import TRANSLATIONS, POLISH_BOOK_NAMES

def create_embed(title: str, message: str, translation: str, verse_count: int) -> discord.Embed:
    description = f"Liczba wersetów: **{verse_count}**\nPrzekład Pisma Świętego: **{translation}**\n\n{message}"
    return discord.Embed(
        title=title,
        description=description,
        color=STANDARD_COLOR
    )

@app_commands.command(name="search", description="Wyszukuje fragmenty zawierające dane słowo lub frazę")
@app_commands.describe(text="Wpisz słowo lub frazę", translation="Wybierz przekład Pisma Świętego")
@app_commands.autocomplete(translation=translation_autocomplete)
async def search(interaction: discord.Interaction, text: str, translation: str = None):
    await interaction.response.defer()

    user_id = interaction.user.id
    user_data = get_user_settings(user_id)

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

    translations = load_json(TRANSLATIONS)
    polish_book_names = load_json(POLISH_BOOK_NAMES)

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

    words = text.split()
    total_verses = count_verses(chosen_translation, words)
    results = search_verses(chosen_translation, words)

    if not results:
        error_embed = discord.Embed(
            title="Błąd",
            description=f'Nie znaleziono wersetów zawierających: **{text}**',
            color=ERROR_COLOR
        )
        await interaction.followup.send(embed=error_embed)
        return

    title = f"Wyniki wyszukiwania dla: {text}"

    embeds = []
    message = ""

    for row in results:
        book_name, book_number, chapter, verse_number, verse_text = row
        polish_book_name = polish_book_names.get(book_name, book_name)

        bold_text = verse_text

        for word in words:
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            bold_text = pattern.sub(lambda m: f"**{m.group(0)}**", bold_text)

        italic_bold_text = italic_font(bold_text)
        passage = f"**{polish_book_name} {chapter}:{verse_number}** \n{italic_bold_text}\n\n"

        if len(message) + len(passage) < 600:
            message += passage
        else:
            embeds.append(create_embed(title, message, translations[chosen_translation], total_verses))
            message = passage

    if message:
        embeds.append(create_embed(title, message, translations[chosen_translation], total_verses))

    view = PaginatorView(embeds)
    await interaction.followup.send(embed=view.initial, view=view)
