import discord

from discord.ext import commands
from colorama import Fore, Style, init
from services.user_settings_db import get_all_user_settings

init(autoreset=True)

default_translations = {}

def setup_ready_event(client: commands.Bot):
    @client.event
    async def on_ready():
        print(f"{Fore.GREEN}[✓]{Style.RESET_ALL} Zalogowano jako: {Fore.CYAN}{client.user}")
        await client.change_presence(activity=discord.Activity(name='Biblię', type=discord.ActivityType.watching))
        
        try:
            synced = await client.tree.sync()
            print(f"{Fore.GREEN}[✓]{Style.RESET_ALL} Zsynchronizowano {Fore.YELLOW}{len(synced)}{Style.RESET_ALL} komend")
        except Exception as e:
            print(f"{Fore.RED}[✗] Błąd synchronizacji komend: {e}")

        rows = get_all_user_settings()
        for user_id, translation in rows:
            default_translations[user_id] = translation