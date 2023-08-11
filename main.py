import settings
import os
import requests
from bs4 import BeautifulSoup
import discord
from discord import app_commands
from discord.ext import commands, tasks

logger = settings.logging.getLogger('bot')

def main():
    bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())
    bot.remove_command('help')

    @bot.event
    async def on_ready():
        logger.info(f'User: {bot.user} (ID: {bot.user.id})')
        try:
            update_presence.start()
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    await bot.load_extension(f'cogs.{filename[:-3]}')
            synced = await bot.tree.sync()
            logger.info(f"Synced: {', '.join(c.name for c in synced)} commands!")
            await bot.change_presence(status=discord.Status.idle, activity=discord.Game(f'Created by FlamesCoder ♡'))
        except Exception as e:
            logger.error(e)
    
    @tasks.loop(seconds=5.0)
    async def update_presence():
        soup = BeautifulSoup(requests.get('https://github.com/FlamesC0der').text, "html.parser")
        data = soup.find_all('span',class_="Counter")
        await bot.change_presence(status=discord.Status.idle, activity=discord.Game(f'Repos: {data[0].text} | Stars: {data[3].text}'))

    bot.run(settings.DISCORD_API_TOKEN,root_logger=True)

if __name__ == "__main__":
    main()
