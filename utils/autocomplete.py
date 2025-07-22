from discord import app_commands, Interaction
from utils.load_json import load_json
from config.paths import TRANSLATIONS, POLISH_BOOK_NAMES

async def translation_autocomplete(
    interaction: Interaction,
    current: str,
) -> list[app_commands.Choice[str]]:
    bible_translations = load_json(TRANSLATIONS)
    return [
        app_commands.Choice(name=full_name, value=abbreviation)
        for abbreviation, full_name in bible_translations.items()
        if current.lower() in full_name.lower()
    ][:25]

async def book_name_autocomplete(
    interaction: Interaction,
    current: str,
) -> list[app_commands.Choice[str]]:
    polish_books_names = load_json(POLISH_BOOK_NAMES)
    return [
        app_commands.Choice(name=book_name, value=key)
        for key, book_name in polish_books_names.items()
        if current.lower() in book_name.lower()
    ][:25]