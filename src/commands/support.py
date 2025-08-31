import discord, os

from dotenv import load_dotenv
from discord import app_commands
from config.colors import STANDARD_COLOR

load_dotenv()

SERVER_LINK = os.getenv("SERVER_LINK")

class InviteView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(label="Dołącz do serwera", url=SERVER_LINK))

@app_commands.command(name="support", description="Serwer wsparcia bota")
async def support(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Serwer wsparcia bota",
        description=(
            "Masz pytania, sugestie lub chcesz zgłosić problem? "
            "Dołącz do naszego serwera wsparcia, gdzie uzyskasz pomoc od społeczności i twórcy bota!"
        ),
        color=STANDARD_COLOR
    )
    view = InviteView()
    await interaction.response.send_message(embed=embed, view=view)
