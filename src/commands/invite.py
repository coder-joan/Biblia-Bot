import discord, os

from dotenv import load_dotenv
from discord import app_commands

load_dotenv()

INVITE_LINK = os.getenv("INVITE_LINK")

class InviteView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(label="Dodaj bota", url=INVITE_LINK))

@app_commands.command(name="invite", description="Dodaj bota na swój serwer")
async def invite(interaction: discord.Interaction):
    view = InviteView()
    await interaction.response.send_message(view=view)