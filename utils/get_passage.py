from utils.load_json import load_json
from config.paths import POLISH_BOOK_NAMES
from services.bibles_db import get_bible_connection, get_passages

def get_passage(translation, book, chapter, start_verse, end_verse):
    polish_book_names = load_json(POLISH_BOOK_NAMES)

    if (start_verse == 0 or end_verse == 0) and start_verse > end_verse:
        return None
    
    conn = get_bible_connection()
    cursor = conn.cursor()

    cursor.execute(get_passages(), (translation, book, chapter, start_verse, end_verse))
    verses = cursor.fetchall()

    if not verses:
        return None

    verses_list = [{"book_name": passage[0], "chapter": passage[1], "verse": passage[2], "text": passage[3]} for passage in verses]

    start_verse = verses_list[0]["verse"]
    end_verse = verses_list[-1]["verse"]

    verses_range = f"{start_verse}" if start_verse == end_verse else f"{start_verse}-{end_verse}"

    polish_book_name = polish_book_names.get(book, book)

    return {
        "book_name": polish_book_name,
        "chapter": chapter,
        "verses_range": verses_range,
        "verses": verses_list
    }