import discord, os

from discord import app_commands
from config.paths import MAPS
from config.colors import STANDARD_COLOR, ERROR_COLOR

MAP_FILE_NAMES = {
    "Kraje podróży Abrahama": "kraje_podrozy_abrahama.jpg",
    "Mapa plemion izraelskich": "mapa_plemion_izraelskich.jpg",
    "Palestyna w czasach Nowego Testamentu": "palestyna_w_czasach_nowego_testamentu.jpg",
    "Podróże Apostoła Pawła": "podroze_apostola_pawla.jpg"
}

@app_commands.command(name="maps", description="Mapy z Biblii")
@app_commands.describe(map="Wybierz mapę")
@app_commands.choices(map=[
    app_commands.Choice(name="Kraje podróży Abrahama", value="Kraje podróży Abrahama"),
    app_commands.Choice(name="Mapa plemion izraelskich", value="Mapa plemion izraelskich"),
    app_commands.Choice(name="Palestyna w czasach Nowego Testamentu", value="Palestyna w czasach Nowego Testamentu"),
    app_commands.Choice(name="Podróże Apostoła Pawła", value="Podróże Apostoła Pawła")
])

async def maps(interaction: discord.Interaction, map: app_commands.Choice[str]):
    await interaction.response.defer()

    file_name = MAP_FILE_NAMES.get(map.value)
    file_path = os.path.join(MAPS, file_name)

    try:
        image = discord.File(file_path, filename='map.jpg')

        embed = discord.Embed(
            title=map.name,
            color=STANDARD_COLOR
        )
        embed.set_image(url="attachment://map.jpg")

        await interaction.followup.send(embed=embed, file=image)

    except FileNotFoundError:
        error_embed = discord.Embed(
            title="Błąd",
            description="Nie znaleziono mapy",
            color=ERROR_COLOR
        )
        await interaction.followup.send(embed=error_embed)