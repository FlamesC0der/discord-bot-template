import discord
from discord import app_commands
from discord.ext import commands


class Economy(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
  
  @app_commands.command(name="set_money", description="Set Money count")
  @app_commands.describe(user="User")
  @app_commands.describe(amount="Amout of cash")
  async def set_money(self, interaction: discord.Interaction, user: discord.User, amount: int = 1000):
    result = self.bot.database.set_money(
      user.id, interaction.guild.id, amount
    )
    await interaction.response.send_message(f"Set {user.name}'s money: {amount}")
  
  @app_commands.command(name="top", description="Get top player's balance")
  async def top(self, interaction: discord.Interaction):
    result = self.bot.database.get_top(
      interaction.guild.id
    )
    data = []
    for i in range(len(result)):
      user = await self.bot.fetch_user(result[i][2])
      data.append(f"{i + 1}) {user.name}....{result[i][3]}")
    embed = discord.Embed(
      title="Top Money",
      description="\n".join(data)
    )
    await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
  await bot.add_cog(Economy(bot))
