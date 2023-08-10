import discord
from discord import app_commands
from discord.ext import commands

class Clear(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    @app_commands.command(name="clear", description="Clears last messages (can take some time)")
    @app_commands.describe(count="Count of messages (1-20, default 10)")
    async def clear(self, interaction: discord.Interaction, count: int = 10):
        if count < 1: count = 1
        if count > 20: count = 20
        await interaction.response.send_message(embed=discord.Embed(title=f"🗑️ Bot cleared {count} message(s)"), ephemeral=True)
        await interaction.channel.purge(limit=count)

async def setup(bot: commands.Bot):
    await bot.add_cog(Clear(bot))
