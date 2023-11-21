import discord
from discord import app_commands
from discord.ext import commands


class Money(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
  
  @app_commands.command(
    name="set_money", description="Set Money count"
  )
  @app_commands.describe(user="User")
  @app_commands.describe(amount="Amout of cash")
  async def set_money(self, interaction: discord.Interaction, user: discord.User, amount: int = 1000):
    result = self.bot.database.set_money(
      user.id, interaction.guild.id, amount
    )
    await interaction.response.send_message(f"Set {user.name}'s money: {amount} ({result})")


async def setup(bot: commands.Bot):
  await bot.add_cog(Money(bot))
