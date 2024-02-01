from typing import Optional
import discord
from discord import app_commands
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ban", description="Ban user")
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(user="User")
    @app_commands.describe(duration="Duration of ban(2h 10m 5s. Permanent if not specified)")
    @app_commands.describe(clear_days="Amount of days to clear user's messages (1 day if not specified)")
    @app_commands.describe(reason="Reason")
    async def ban(self, interaction: discord.Interaction, user: discord.User, duration: str = "permanent",
                  clear_days: int = 1, reason: str = "No reason spicified"):
        user = interaction.guild.get_member(user.id) or await self.bot.fetch_user(user.id)
        try:
            try:
                # Try to send private ban message
                await user.send(embed=discord.Embed(title="Banned", description=f"""Hi, {user.global_name}!
Unfortunately you have been banned from {interaction.guild.name}.

**Reason**: {reason}
**Moderator**: {interaction.user.global_name}
**Duration**: {duration}""", color=0xad1457))
            except:
                pass
            await interaction.guild.ban(user=user, reason=reason, delete_message_days=clear_days)
            await interaction.response.send_message(
                embed=discord.Embed(title=f"Successfully banned {user.name}", color=0xad1457))
        except:
            await interaction.response.send_message(
                embed=discord.Embed(title="An error occurred while trying to ban the user.", color=0xad1457))

    @app_commands.command(name="unban", description="Unban user")
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(user_id="User id")
    async def unban(self, interaction: discord.Interaction, user_id: str):
        try:
            user = interaction.guild.get_member(user_id) or await self.bot.fetch_user(user_id)
            try:
                await interaction.guild.unban(user)
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"Successfully unbanned {user_id}", color=0xad1457))
            except:
                await interaction.response.send_message(
                    embed=discord.Embed(title="An error occurred while trying to ban the user.", color=0xad1457))
        except:
            await interaction.response.send_message(embed=discord.Embed(title="User not found", color=0xad1457))

    @app_commands.command(name="kick", description="Kick user from server")
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(user="User")
    @app_commands.describe(reason="Reason")
    async def kick(self, interaction: discord.Integration, user: discord.User, reason: str = "No reason spicified"):
        try:
            try:
                await user.send(embed=discord.Embed(title="Kicked", description=f"""Hi, {user.global_name}!
Unfortunately you have been kicked from {interaction.guild.name}.

**Reason**: {reason}
**Moderator**: {interaction.user.global_name}""", color=0xad1457))
            except:
                pass
            await interaction.guild.kick(user=user, reason=reason)
            await interaction.response.send_message(
                embed=discord.Embed(title=f"Successfully kicked {user.name}", color=0xad1457))
        except:
            await interaction.response.send_message(
                embed=discord.Embed(title="An error occurred while trying to kick the user.", color=0xad1457))


async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
