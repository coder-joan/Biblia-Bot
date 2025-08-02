# 📖 Biblia Bot - twój towarzysz do studiowania Biblii na Discordzie
---
## ⚙️ Funkcje bota

- 📅 wysyłanie wersetu dnia
- 🎲 wysyłanie losowego wersetu
- 🔍 wyszukiwanie fragmentów w Biblii
- 📖 możliwość używania skrótów ksiąg
- 🔁 automatyzacja wysyłania wersetu dnia
- 📚 ustawienie domyślnego przekładu Pisma Świętego
- 📑 porównanie fragmentu w różnych przekładach Pisma Świętego
---
## 📂 Instalacja pakietów

``` python
pip install discord.py
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

``` python
pip install pytz
```
---
## 📝 Uzupełnienie danych

### Utwórz plik `.env` z podaną strukturą

``` python
TOKEN='token_bota'
INVITE_LINK='link_z_zaproszeniem'
SERVER_LINK='link_do_serwera_supportu'
```
### Tworzenie linku z zaproszeniem

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
---
## Uruchomienie bota

``` python
python main.py
```
