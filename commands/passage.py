import discord, re

from discord import app_commands
from services.bibles_db import get_verses
from services.user_translation_db import get_user_settings
from config.colors import STANDARD_COLOR, ERROR_COLOR
from config.paths import TRANSLATIONS, POLISH_BOOK_NAMES
from utils.load_json import load_json
from utils.italic_font import italic_font
from utils.autocomplete import translation_autocomplete, book_name_autocomplete

@app_commands.command(name="passage", description="Wyświetla fragment z Pisma Świętego")

@app_commands.describe(
    book="Wybierz księgę",
    chapter="Wpisz numer rozdziału",
    verses="Wpisz zakres wersetów np. 16-17",
    translation="Wybierz przekład Pisma Świętego",
)

@app_commands.autocomplete(
    translation=translation_autocomplete, 
    book=book_name_autocomplete
)

async def passage(
    interaction: discord.Interaction,
    book: str,
    chapter: int,
    verses: str,
    translation: str = None
):
    await interaction.response.defer()

    translations = load_json(TRANSLATIONS)
    polish_book_names = load_json(POLISH_BOOK_NAMES)

    polish_book_name = polish_book_names.get(book, book)

    user_id = interaction.user.id
    user_data = get_user_settings(user_id)

    if book not in polish_book_names:
        error_embed = discord.Embed(
            title="Błąd",
            description=(
                f"Podano błędną nazwę księgi"
            ),
            color=ERROR_COLOR
        )
        await interaction.followup.send(embed=error_embed)
        return

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
    
    match = re.match(r"^(\d+)(?:-(\d+))?$", verses)

    if not match:
        error_embed=discord.Embed(
            title="Błąd",
            description="Podano nieprawidłowy format wersetów. Wpisz np. `1` lub `1-3`",
            color=ERROR_COLOR
        )
        await interaction.followup.send(embed=error_embed)
        return

    start_verse = int(match.group(1))
    end_verse = int(match.group(2)) if match.group(2) else start_verse

    verse = get_verses(chosen_translation, book, chapter, start_verse, end_verse)

    passage = f"{polish_book_name} {chapter}:{verses}"

    if not verse:
        error_embed = discord.Embed(
            title="Błąd wyszukiwania",
            description=(
                    "Poniżej przedstawiono możliwe przyczyny błędu:\n\n"

                    "- werset nie istnieje\n"
                    "- przekład nie zawiera danej księgi\n"
                    "- przekład nie zawiera Starego lub Nowego Testamentu\n\n"
                    
                    "Upewnij się, że wprowadzone dane są prawidłowe i spróbuj jeszcze raz"
                ),
            color=ERROR_COLOR
        )
        await interaction.followup.send(embed=error_embed)
        return
    
    def format_passage(verses_list):
        return " ".join(
            f"**({verse_number})** {italic_font(text)}" for verse_number, text in verses_list
        )

    embed = discord.Embed(
        title=f"{passage}",
        description=(
            f"{format_passage(verse)}"
        ),
        color=STANDARD_COLOR
    )
    embed.set_footer(text=translations[chosen_translation])
    await interaction.followup.send(embed=embed)
