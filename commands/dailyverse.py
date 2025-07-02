import discord, requests

from bs4 import BeautifulSoup
from discord import app_commands
from utils.load_json import load_json
from utils.italic_font import italic_font
from utils.get_passage import get_passage
from services.user_settings_db import get_user_settings
from config.colors import STANDARD_COLOR, ERROR_COLOR
from config.paths import TRANSLATIONS, ALTERNATIVE_BOOK_NAMES, POLISH_BOOK_NAMES

def get_canonical_book_name(book, books):
    for canonical_book_name, aliases in books.items():
        if book in aliases:
            return canonical_book_name
    return book

@app_commands.command(name="dailyverse", description="Wyświetla werset dnia z Biblii")
async def dailyverse(interaction: discord.Interaction):
    await interaction.response.defer()

    user_id = interaction.user.id
    user_data = get_user_settings(user_id)

    if not user_data:
        embed = discord.Embed(
            title="Ustaw domyślny przekład Pisma Świętego",
            description=(
                'Zanim rozpoczniesz wyszukiwanie fragmentów w Biblii, '
                'ustaw domyślny przekład Pisma Świętego za pomocą komendy `/setversion`'
            ),
            color=STANDARD_COLOR
        )
        await interaction.followup.send(embed=embed, ephemeral=True)
        return

    translation = user_data[1]

    try:
        polish_book_names = load_json(POLISH_BOOK_NAMES)
        bible_translations = load_json(TRANSLATIONS)
        books = load_json(ALTERNATIVE_BOOK_NAMES)

        response = requests.get("https://www.verseoftheday.com/")
        soup = BeautifulSoup(response.text, 'html.parser')
        reference_div = soup.find("div", class_="reference")
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

        passage = get_passage(translation, canonical_book_name, chapter, start_verse, end_verse)

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
        embed.set_footer(text=bible_translations.get(translation, translation))
        await interaction.followup.send(embed=embed)

    except Exception as e:
        error_embed = discord.Embed(
            title="Błąd",
            description="Nie znaleziono wersetu",
            color=ERROR_COLOR
        )
        await interaction.followup.send(embed=error_embed, ephemeral=True)