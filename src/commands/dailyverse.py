import discord, requests

from discord import app_commands
from bs4 import BeautifulSoup
from utils.load_json import load_json
from utils.italic_font import italic_font
from utils.get_passage import get_passage
from utils.autocomplete import translation_autocomplete
from services.user_translation_db import get_user_settings
from services.dailyverse_settings_db import get_dailyverse_settings
from config.colors import STANDARD_COLOR, ERROR_COLOR
from config.paths import TRANSLATIONS, ALTERNATIVE_BOOK_NAMES, POLISH_BOOK_NAMES

def get_canonical_book_name(book, books):
    for canonical_book_name, aliases in books.items():
        if book in aliases:
            return canonical_book_name
    return book

@app_commands.command(name="dailyverse", description="Wyświetla werset dnia")
@app_commands.describe(translation="Wybierz przekład Pisma Świętego")
@app_commands.autocomplete(translation=translation_autocomplete)
async def dailyverse(interaction: discord.Interaction, translation: str = None):
    await interaction.response.defer()

    polish_book_names = load_json(POLISH_BOOK_NAMES)
    bible_translations = load_json(TRANSLATIONS)
    books = load_json(ALTERNATIVE_BOOK_NAMES)

    user_id = interaction.user.id
    guild_id = interaction.guild.id

    user_settings = get_dailyverse_settings(user_id, guild_id)
    channel_id, hour, timezone = (user_settings if user_settings else (None, None, None))
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
    
    if chosen_translation not in bible_translations:
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

    try:
        response = requests.get("https://www.biblestudytools.com/bible-verse-of-the-day/")
        soup = BeautifulSoup(response.text, 'html.parser')
        reference_div = soup.find("div", class_="w-full mb-5")
        link = reference_div.find("a", href=True)
        verse_reference = link.text.strip()

        book, chapter_verse = verse_reference.rsplit(" ", 1)
        chapter, verses = chapter_verse.split(":")
        chapter = int(chapter)

        verse_range = verses.split("-")
        start_verse = int(verse_range[0])
        end_verse = int(verse_range[1]) if len(verse_range) > 1 else start_verse

        canonical_book_name = get_canonical_book_name(book, books)
        polish_book_name = polish_book_names.get(book, book)

        passage = get_passage(chosen_translation, canonical_book_name, chapter, start_verse, end_verse)

        if not passage:
            error_embed = discord.Embed(
                title="Błąd",
                description="Nie znaleziono wersetu w bazie danych",
                color=ERROR_COLOR
            )
            await interaction.followup.send(embed=error_embed, ephemeral=True)

        title = f"{polish_book_name} {chapter}:{start_verse}" if start_verse == end_verse else f"{polish_book_name} {chapter}:{start_verse}-{end_verse}"

        desc = ""
        for verse in passage["verses"]:
            verse_text = italic_font(verse["text"]).replace("\n", " ").replace("  ", " ").strip()
            desc += f"**({verse['verse']})** {verse_text} "

        desc = (desc[:4093] + '...') if len(desc) > 4093 else desc

        embed = discord.Embed(
            title=title,
            description=desc,
            color=STANDARD_COLOR
        )
        embed.set_footer(text=bible_translations.get(chosen_translation, chosen_translation))
        await interaction.followup.send(embed=embed)

    except Exception as e:
        error_embed = discord.Embed(
            title="Błąd",
            description="Nie znaleziono wersetu",
            color=ERROR_COLOR
        )
        await interaction.followup.send(embed=error_embed, ephemeral=True)
