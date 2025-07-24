# Biblia Bot - twój towarzysz do studiowania Biblii na Discordzie

## Funkcje bota

* 📅 wysyłanie wersetu dnia z Biblii
* 🔍 wyszukiwanie fragmentów w Biblii
* 📖 możliwość używania skrótów ksiąg
* 🎲 wysyłanie losowego wersetu z Biblii
* 📚 ustawienie domyślnego przekładu Pisma Świętego
* 📑 porównanie fragmentu w różnych przekładach Pisma Świętego

## Instalacja pakietów

* Wpisz w terminalu następujące komendy:

``` python
pip install discord.py
```

``` python
pip install asyncio
```

``` python
pip install pysqlite3
```

``` python
pip install python-dotenv
```

``` python
pip install beautifulsoup4
```

``` python
pip install requests
```

## Utwórz plik `.env` z podaną strukturą

``` python
TOKEN='token_bota'
SERVER_LINK='link_do_serwera'
INVITE_LINK='link_z_zaproszeniem'
```
## Tworzenie linku z zaproszeniem

Link z zaproszeniem należy utworzyć w **Discord Developer Portal**
1. Wejdź w aplikację bota
2. Kliknij w zakładkę **OAuth2**
3. W **SCOPES** zaznacz `bot` i `applications.commands`
4. W **BOT PERMISSIONS** zaznacz następujące uprawnienia:
* View Channels
* Send Messages
* Send Messages in Threads
* Use Slash Commands
* Manage Messages
* Embed Links

## Baza danych

W folderze `data` zostanie utworzona baza danych w pliku `user_settings.db` gdy pierwszy użytkownik ustawi domyślny przekład Pisma Świętego

## Uruchomienie bota

* Wpisz w terminalu następującą komendę:

``` python
python main.py
```
