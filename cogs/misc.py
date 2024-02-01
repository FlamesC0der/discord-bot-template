import discord
import asyncio
from discord import app_commands
from discord.ext import commands
import wavelink


class Misc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def whitelist(interaction):
        users = [760230155150426146]
        return interaction.user.id in users

    @app_commands.command(name="say", description="Make the bot say something")
    @app_commands.describe(message="What should i say")
    async def say(self, interaction: discord.Interaction, message: str):
        await interaction.response.send_message(message)

    @app_commands.command(name="ping", description="Returns bot ping")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=discord.Embed(description="Bot ping..."), ephemeral=True)
        if interaction.guild:
            vc: wavelink.Player = interaction.guild.voice_client
            await interaction.edit_original_response(
                embed=discord.Embed(
                    description=f"Discord Websocket ⇒ `{round(self.bot.latency * 1000, 0)}ms`\nWavelink ⇒ `{vc.ping if vc else '0'}ms`",
                    color=0xad1457
                ),
            )
        else:
            await interaction.edit_original_response(
                embed=discord.Embed(
                    description=f"Discord Websocket ⇒ `{round(self.bot.latency * 1000, 0)}ms`",
                    color=0xad1457
                ),
            )

    @app_commands.command(name="clear", description="Clears last messages (can take some time)")
    @app_commands.guild_only()
    @app_commands.describe(count="Count of messages (default 10)")
    async def clear(self, interaction: discord.Interaction, count: int):
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
                color=0xad1457
            )
        )
        await asyncio.sleep(0.5)
        await interaction.edit_original_response(
            embed=discord.Embed(
                title=f"✅ Deleted {len(deleted_msg)} message(s)",
                color=0xad1457
            ),
        )
        await asyncio.sleep(10)
        await msg.delete()

    @app_commands.command(name="ny", description="NY")
    @app_commands.check(whitelist)
    async def ny(self, interaction: discord.Integration):
        members = set()

        async for guild in self.bot.fetch_guilds(limit=100):
            async for member in guild.fetch_members():
                members.add(member.id)

        print(members)
        await interaction.channel.send(members)

        for user_id in members:
            user = await self.bot.fetch_user(user_id)
            try:
                await user.send(embed=discord.Embed(description=f"""Дорогой {user.name},

От лица FlameCoderDev, я хотел бы поздравить тебя с наступающим Новым Годом! Желаю тебе, чтобы год был наполнен яркими моментами, великими достижениями и невероятными успехами.

Пусть Новый Год принесет тебе обновления, новые достижения и незабываемые приключения.

Счастливого Нового Года, {user.name}! Желаю тебе вдохновения, мощных навыков и непреодолимой силы во всем, что ты предпримешь. Продолжай непрерывно творить и захватывать нас своим исполнением.

С наилучшими пожеланиями,
FlameCoderDeb"""))
                print(f"message sent to {user.name}")
            except Exception as e:
                print(f"Failed to send message to {user.name}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Misc(bot))
