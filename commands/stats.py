import discord

from discord.ext import commands
from config.colors import STANDARD_COLOR
from services.user_settings_db import get_user_count

@commands.command(name="stats")
async def stats(ctx):
    embed = discord.Embed(
        title="Statystyki",
        description=f"Liczba serwerów: **{len(ctx.bot.guilds)}**\n"
                    f"Liczba użytkowników: **{get_user_count()}**",
        color=STANDARD_COLOR
    )
    await ctx.send(embed=embed)