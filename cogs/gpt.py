import discord
import requests
import asyncio
from discord import app_commands
from discord.ext import commands


class Gpt(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
  
  def whitelist(interaction):
    users = [760230155150426146]
    return interaction.user.id in users
  
  @app_commands.command(name="gpt", description="Chat gpt")
  @app_commands.check(whitelist)
  @app_commands.describe(question="Your question")
  async def gpt(self, interaction: discord.Interaction, question: str):
    await interaction.response.send_message(embed=discord.Embed(description="Sending question to openai.com...", color=0xad1457))
    answer = requests.get("https://flamescoderapi--flamesc0der.repl.co/gpt", {"question": question}).json()
    embed = discord.Embed(
      description=answer['result']['content']2,
      color=0xad1457
    )
    embed.set_author(name="ChatGpt3", icon_url="https://media.discordapp.net/attachments/1131242153155231948/1183535435113300049/gpt.png?ex=6588b044&is=65763b44&hm=e6617bedd3b13a2d2279a01d4297ac54338ad9d0928b08a9dd4237ca3ead4c2e&=&format=webp&quality=lossless&width=200&height=200")
    await interaction.edit_original_response(
      embed=embed
    )
  
  @gpt.error
  async def gpt_error(self, interaction, error):
    print(error)
    if isinstance(error, app_commands.CheckFailure):
      await interaction.response.send_message(embed=discord.Embed(description="Sorry, you have been blocked", color=0xad1457))


async def setup(bot: commands.Bot):
  await bot.add_cog(Gpt(bot))
