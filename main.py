import settings
import os
import discord
from discord import app_commands
from discord.ext import commands

logger = settings.logging.getLogger('bot')

def main():
    bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())
    bot.remove_command('help')

    @bot.event
    async def on_ready():
        logger.info(f'User: {bot.user} (ID: {bot.user.id})')
        try:
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    await bot.load_extension(f'cogs.{filename[:-3]}')
            synced = await bot.tree.sync()
            logger.info(f"Synced: {', '.join(c.name for c in synced)} commands!")
            await bot.change_presence(status=discord.Status.online, activity=discord.Game(f'/help'))
        except Exception as e:
            logger.error(e)

    bot.run(settings.DISCORD_API_TOKEN,root_logger=True)

if __name__ == "__main__":
    main()
