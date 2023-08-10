import discord
from discord import app_commands
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    @app_commands.command(name="ping", description="Returns bot ping")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=discord.Embed(title=f'Pong!\n🌐 {round(self.bot.latency, 4)}ms'), ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Ping(bot))
