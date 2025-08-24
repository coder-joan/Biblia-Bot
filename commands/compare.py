import discord, re

from discord import app_commands
from utils.load_json import load_json
from services.bibles_db import get_verses
from config.colors import STANDARD_COLOR, ERROR_COLOR
from config.paths import TRANSLATIONS, POLISH_BOOK_NAMES
from utils.italic_font import italic_font
from utils.autocomplete import translation_autocomplete, book_name_autocomplete

@app_commands.command(name="compare", description="Porównuje fragment w różnych przekładach Pisma Świętego")

@app_commands.describe(
    book="Wybierz księgę",
    chapter="Wpisz numer rozdziału",
    verses="Wpisz zakres wersetów np. 16-17",
    translation_1="Wybierz pierwszy przekład Pisma Świętego",
    translation_2="Wybierz drugi przekład Pisma Świętego"
)

@app_commands.autocomplete(
    translation_1=translation_autocomplete, 
    translation_2=translation_autocomplete, 
    book=book_name_autocomplete
)

async def compare(
    interaction: discord.Interaction,
    book: str,
    chapter: int,
    verses: str,
    translation_1: str,
    translation_2: str
):
    await interaction.response.defer()

    translations = load_json(TRANSLATIONS)
    polish_book_names = load_json(POLISH_BOOK_NAMES)

    polish_book_name = polish_book_names.get(book, book)

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

    if translation_1 not in translations or translation_2 not in translations:
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

    verse_1 = get_verses(translation_1, book, chapter, start_verse, end_verse)
    verse_2 = get_verses(translation_2, book, chapter, start_verse, end_verse)

    verse = f"{polish_book_name} {chapter}:{verses}"

    if not verse_1 or not verse_2:
        error_embed = discord.Embed(
            title="Błąd",
            description=f"Nie znaleziono wersetu",
            color=ERROR_COLOR
        )
        await interaction.followup.send(embed=error_embed)
        return
    
    def format_passage(verses_list):
        return " ".join(
            f"**({verse_number})** {italic_font(text)}" for verse_number, text in verses_list
        )

    embed = discord.Embed(
        title=f"Porównanie fragmentu: {verse}",
        description=(
            f"**{translations[translation_1]}**\n{format_passage(verse_1)}\n\n"
            f"**{translations[translation_2]}**\n{format_passage(verse_2)}"
        ),
        color=STANDARD_COLOR
    )
    await interaction.followup.send(embed=embed)
