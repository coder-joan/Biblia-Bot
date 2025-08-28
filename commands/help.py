import discord

from discord import app_commands
from config.colors import STANDARD_COLOR
from utils.paginator_view import PaginatorView

@app_commands.command(name="help", description="Pomoc")
async def help(interaction: discord.Interaction):
    description = [
        f'Zanim rozpoczniesz wyszukiwanie fragmentów w Biblii, '
         'ustaw domyślny przekład Pisma Świętego za pomocą komendy `/setversion`\n\n'

         '**Schemat wyszukiwania fragmentów w Biblii:**\n'
         '- `[księga] [rozdział]:[wersety] [przekład]`\n\n'

         '**Przykłady:**\n'
         '- `Jana 3:16` - pojedynczy werset\n'
         '- `Jana 3:1-8` - zakres wersetów\n'
         '- `Jana 1:12-13 UBG` - zakres wersetów z przekładem Pisma Świętego\n\n'

         'Jeśli masz ustawiony domyślny przekład Pisma Świętego, nie musisz podawać jego skrótu',

        f'Lista dostępnych komend:\n\n'

         '- `/maps` - wyświetla wybraną mapę\n'
         '- `/random` - wyświetla losowy werset\n'
         '- `/dailyverse` - wyświetla werset dnia\n'
         '- `/information` - wyświetla informacje o bocie\n'
         '- `/passage` - wyświetla fragment z Pisma Świętego\n'
         '- `/invite` - umożliwia dodanie bota na swój serwer\n'
         '- `/setdailyverse` - ustawia automatyzację wersetu dnia\n'
         '- `/cleardailyverse` - usuwa automatyzację wersetu dnia\n'
         '- `/mysettings` - wyświetla bieżące ustawienia użytkownika\n'
         '- `/setversion` - ustawia domyślny przekład Pisma Świętego\n'
         '- `/versions` - wyświetla dostępne przekłady Pisma Świętego\n'
         '- `/cleartranslation` - usuwa domyślny przekład Pisma Świętego\n'
         '- `/search` - wyszukuje fragmenty zawierające dane słowo lub frazę\n'
         '- `/compare` - porównuje fragment w różnych przekładach Pisma Świętego\n\n'

         'Masz pytania lub sugestie? Użyj komendy `/support` i daj znać autorowi bota'
    ]
    embeds = [discord.Embed(title="Pomoc", description=desc, color=STANDARD_COLOR) for desc in description]
    view = PaginatorView(embeds)
    await interaction.response.send_message(embed=view.initial, view=view)
