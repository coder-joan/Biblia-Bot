import discord

from discord import app_commands
from config.colors import STANDARD_COLOR

@app_commands.command(name="information", description="Informacje o bocie")
async def information(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Informacje",
        description=(
            "**Biblia** to bot, który umożliwia czytanie Pisma Świętego w wielu językach "
            "oraz porównywanie tekstów oryginalnych z ich tłumaczeniami\n\n"

            "Przekłady są dostępne w **6** językach: **polskim**, **angielskim**, "
            "**niemieckim**, **łacińskim**, **greckim** i **hebrajskim**\n\n"
                    
            "**Strona internetowa:** https://biblia-bot.netlify.app/\n\n"
                    
            "[Warunki korzystania z usług bota](https://biblia-bot.netlify.app/terms-of-service) • [Polityka Prywatności](https://biblia-bot.netlify.app/privacy-policy)"
        ),
        color=STANDARD_COLOR)

    await interaction.response.send_message(embed=embed)