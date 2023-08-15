import os
import asyncio
import datetime
import json
import random

import logging
import discord
from discord.ext import commands, tasks


# Load config
with open("config.json", "r") as f:
    config = json.load(f)


# Logger
class LoggingFormatter(logging.Formatter):
    black = "\x1b[30m"
    FAIL = "\033[91m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    gray = "\x1b[38m"
    reset = "\x1b[0m"

    format = "[%(asctime)s] %(levelname)-8s | %(module)-15s | %(message)s"

    FORMATS = {
        logging.DEBUG: gray + format + reset,
        logging.INFO: blue + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: FAIL + format + reset,
    }

    def format(self, record):
        formatter = logging.Formatter(self.FORMATS.get(record.levelno))
        return formatter.format(record)


logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)

logging.getLogger("discord.http").setLevel(logging.INFO)
discord.VoiceClient.warn_nacl = False  # Disable PyNaCl Warning

console_handler = logging.StreamHandler()
console_handler.setFormatter(LoggingFormatter())
file_handler = logging.FileHandler(
    filename=f"logs/{datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}.log",
    mode="w",
)
file_handler.setFormatter(
    logging.Formatter("[%(asctime)s] %(levelname)-8s | %(module)-15s | %(message)s")
)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Intents

intents = discord.Intents.default()
# Privileged Intents (Needs to be enabled on developer portal of Discord (https://discord.com/developers/applications)), please use them only if you need them:
# intents.members = True
# intents.message_content = True
# intents.presences = True


bot = commands.Bot(
    command_prefix=config["prefix"],
    help_command=None,
    intents=intents,
)


@bot.event
async def on_ready():
    logger.info(f"User: {bot.user} (ID: {bot.user.id})")
    update_presence.start()
    await bot.tree.sync()
    await bot.change_presence(
        status=discord.Status.idle,
        activity=discord.Game(f"Created by FlamesCoder ♡"),
    )


@tasks.loop(minutes=1.0)
async def update_presence():
    await bot.change_presence(
        status=discord.Status.idle,
        activity=discord.Game(
            random.choice(["Created by FlamesCoder ♡", f"Guilds: {len(bot.guilds)}"])
        ),
    )


async def load_cogs():
    logger.info("Loading cogs:")
    logger.info("---------------------------")
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                logger.info(f"Loaded extension: {filename[:-3]}")
            except Exception as e:
                logger.error(
                    f'Failed to load extension {filename[:-3]}\n{f"{type(e).__name__}: {e}"}'
                )
    logger.info("---------------------------")


asyncio.run(load_cogs())
bot.run(config["token"], log_handler=None)
