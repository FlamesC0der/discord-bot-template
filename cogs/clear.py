import asyncio
import discord
from discord import app_commands
from discord.ext import commands


class Clear(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="clear", description="Clears last messages (can take some time)"
    )
    @app_commands.describe(count="Count of messages (default 10)")
    async def clear(self, interaction: discord.Interaction, count: int = 10):
        def progressBar(iteration, total):
            percent = iteration / total * 100
            filledLength = int(10 * iteration // total)
            bar = (
                "<:l2:1139611778771329205>" * filledLength
                + "<:l1:1139611748131934208>" * (10 - filledLength)
            )
            return f"{round(percent, 2)}% | {bar} | {iteration}/{total}\nPlease wait..."

        await interaction.response.send_message(
            embed=discord.Embed(
                title=f"Clearing messages:", description=f"{progressBar(0, count)}"
            )
        )
        msg = await interaction.original_response()

        deleted_msg = await interaction.channel.purge(
            limit=count + 1, check=lambda m: m.id != msg.id
        )
        await interaction.edit_original_response(
            embed=discord.Embed(
                title=f"Clearing messages:",
                description=f"{progressBar(len(deleted_msg), count)}",
            )
        )
        await asyncio.sleep(0.5)
        await interaction.edit_original_response(
            embed=discord.Embed(title=f"✅ Deleted {len(deleted_msg)} message(s)")
        )
        await asyncio.sleep(10)
        await msg.delete()


async def setup(bot: commands.Bot):
    await bot.add_cog(Clear(bot))
