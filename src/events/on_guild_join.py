import discord, os

from dotenv import load_dotenv
from colorama import Fore, init
from discord.ext import commands
from config.colors import STANDARD_COLOR

load_dotenv()
init(autoreset=True)

SERVER_LINK = os.getenv("SERVER_LINK")

class InviteView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(label="Dołącz do serwera wsparcia bota", url=SERVER_LINK))

def setup_guild_join_event(client: commands.Bot):
    @client.event
    async def on_guild_join(guild):
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                embed = discord.Embed(
                    title="Dziękuję za dodanie Biblia Bot!",
                    description=(
                        "Cieszę się, że mogę być częścią Twojego serwera!\n\n"

                        "**Funkcje bota:**\n"
                        "- 📅 wysyłanie wersetu dnia\n"
                        "- 🎲 wysyłanie losowego wersetu\n"
                        "- 🔍 wyszukiwanie fragmentów w Biblii\n"
                        "- 📖 możliwość używania skrótów ksiąg\n"
                        "- 🔁 automatyzacja wysyłania wersetu dnia\n"
                        "- 📚 ustawienie domyślnego przekładu Pisma Świętego\n"
                        "- 📑 porównanie fragmentu w różnych przekładach Pisma Świętego\n\n"

                        "**Pierwsze kroki:**\n"
                        "1. Ustaw domyślny przekład Pisma Świętego: `/setversion`\n"
                        "2. Skonfiguruj automatyczne wysyłanie wersetu dnia: `/setdailyverse`\n\n"
                        
                        "Masz pytania, sugestie lub chcesz zgłosić problem? **Dołącz do serwera wsparcia**, gdzie uzyskasz pomoc od społeczności i twórcy bota!"
                    ),
                    color=STANDARD_COLOR
                )

                view = InviteView()
                
                try:
                    await channel.send(embed=embed, view=view)
                except discord.errors.Forbidden:
                    print(f"{Fore.RED}[X] Błąd podczas wysyłania wiadomości na serwer: Missing Permissions")
                except Exception as e:
                    print(f"{Fore.RED}[X] Nieoczekiwany błąd w on_guild_join: {e}")
                break