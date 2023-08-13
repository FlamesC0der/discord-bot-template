import discord
from discord import app_commands
from discord.ext import commands


class Say(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="say", description="Make the bot say something")
    @app_commands.describe(message="What should i say")
    async def say(self, interaction: discord.Interaction, message: str):
        await interaction.response.send_message(message)


async def setup(bot: commands.Bot):
    await bot.add_cog(Say(bot))
