import discord

from discord import app_commands
from config.colors import STANDARD_COLOR
from utils.paginator_view import PaginatorView

@app_commands.command(name="versions", description="Dostępne przekłady Pisma Świętego")
async def versions(interaction: discord.Interaction):
    description = [
        f'Poniżej znajdziesz listę wszystkich dostępnych przekładów Pisma Świętego, które możesz '
         'wykorzystać w komendach bota:\n\n'

         '**Polskie:**\n\n'

         '`BB` - Biblia Brzeska (1563)\n'
         '`BN` - Biblia Nieświeska (1574)\n'
         '`BJW` - Biblia Jakuba Wujka (1599)\n'
         '`BG` - Biblia Gdańska (1881)\n'
         '`BS` - Biblia Szwedzka (1948)\n'
         '`BM` - Biblia Mesjańska (1975)\n'
         '`BP` - Biblia Poznańska (1975)\n'
         '`BW` - Biblia Warszawska (1975)\n'
         '`SZ` - Słowo Życia (1989)\n'
         '`BL` - Biblia Lubelska (1991)',

        f'Poniżej znajdziesz listę wszystkich dostępnych przekładów Pisma Świętego, które możesz '
         'wykorzystać w komendach bota:\n\n'

         '`BWP` - Biblia Warszawsko-Praska (1997)\n'
         '`PNS` - Przekład Nowego Świata (1997)\n'
         '`BT` - Biblia Tysiąclecia: wydanie V (1999)\n'
         '`SNPD` - Słowo Nowego Przymierza: przekład dosłowny (2004)\n'
         '`GOR` - Biblia Góralska (2005)\n'
         '`NBG` - Nowa Biblia Gdańska (2012)\n'
         '`PAU` - Biblia Paulistów (2016)\n'
         '`UBG` - Uwspółcześniona Biblia Gdańska (2017)\n'
         '`BE` - Biblia Ekumeniczna (2018)\n'
         '`SNP` - Słowo Nowego Przymierza: przekład literacki (2018)\n'
         '`TNP` - Przekład Toruński Nowego Przymierza (2020)\n'
         '`TRO` - Textus Receptus Oblubienicy (2023)',

        f'Poniżej znajdziesz listę wszystkich dostępnych przekładów Pisma Świętego, które możesz '
         'wykorzystać w komendach bota:\n\n'

         '**Łacińskie:**\n\n'

         '`VG` - Wulgata\n\n'

         '**Greckie:**\n\n'

         '`LXX` - Septuaginta\n'
         '`TR` - Textus Receptus (1550)\n'
         '`NE` - Nestle (1904)\n'
         '`BYZ` - Tekst Bizantyjski (2013)\n\n'

         '**Hebrajskie:**\n\n'

         '`ALEP` - Aleppo Codex\n'
         '`WLC` - Westminster Leningrad Codex'
    ]
    embeds = [discord.Embed(title="Dostępne przekłady Pisma Świętego", description=desc, color=STANDARD_COLOR) for desc in description]
    view = PaginatorView(embeds)
    await interaction.response.send_message(embed=view.initial, view=view)