import discord
from discord import app_commands
from discord.ext import commands

class Button(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    @app_commands.command(name="button", description="Test command")
    async def button(self, interaction: discord.Interaction):
        view = discord.ui.View()
        button = discord.ui.Button(label="click")
        view.add_item(button)
        await interaction.response.send_message(view=view)

async def setup(bot: commands.Bot):
    await bot.add_cog(Button(bot))
