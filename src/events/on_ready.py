import discord

from discord.ext import commands
from colorama import Fore, Style, init
from tasks.dailyverse_task import start_dailyverse_task

init(autoreset=True)

def setup_ready_event(client: commands.Bot):
    @client.event
    async def on_ready():
        print(f"{Fore.GREEN}[✓]{Style.RESET_ALL} Zalogowano jako: {Fore.CYAN}{client.user}")
        await client.change_presence(activity=discord.Activity(name='Biblię', type=discord.ActivityType.watching))
        
        try:
            synced = await client.tree.sync()
            print(f"{Fore.GREEN}[✓]{Style.RESET_ALL} Zsynchronizowano {Fore.YELLOW}{len(synced)}{Style.RESET_ALL} komend")
        except Exception as e:
            print(f"{Fore.RED}[X] Błąd synchronizacji komend: {e}")

        start_dailyverse_task(client)