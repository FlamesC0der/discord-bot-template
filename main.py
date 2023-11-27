import os
import sys
import datetime
import json
import random

import logging
import discord
import wavelink
import sqlite3
from discord.ext import commands, tasks
from dotenv import load_dotenv
from database import DatabaseManager


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
  logging.Formatter("[%(asctime)s] %(levelname)-8s | %(module)-10s | %(message)s")
)

logger.addHandler(console_handler)
logger.addHandler(file_handler)


# Load config

if not os.path.isfile(f"{os.path.realpath(os.path.dirname(__file__))}/config.json"):
  logger.error("There is no file config.json")
  sys.exit()
else:
  with open(f"{os.path.realpath(os.path.dirname(__file__))}/config.json", "r") as f:
    config = json.load(f)


# Intents

intents = discord.Intents.default()
# Privileged Intents (Needs to be enabled on developer portal of Discord (https://discord.com/developers/applications)), please use them only if you need them:
# intents.members = True
# intents.message_content = True
# intents.presences = True

class Bot(commands.Bot):
  def __init__(self) -> None:
    super().__init__(
      command_prefix=config["prefix"],
      help_command=None,
      intents=intents
    )

    self.logger = logger
    self.config = config
    self.database = None
  
  async def setup_hook(self) -> None:
    self.logger.info(f"User: {bot.user} (ID: {bot.user.id})")
    self.logger.info(f"Shard: {bot.shard_id}")
    self.database = DatabaseManager(
      connection=sqlite3.connect(
        f"{os.path.realpath(os.path.dirname(__file__))}/database/database.db"
      )
    )
    await self.init_db()
    await self.load_cogs()
    await self.tree.sync()
    self.update_presence.start()
    node = wavelink.Node(
      uri="http://localhost:2333",
      password="youshallnotpass"
    )
    await wavelink.NodePool.connect(client=self, nodes=[node])
  
  async def init_db(self) -> None:
    with open(f"{os.path.realpath(os.path.dirname(__file__))}/database/build.sql") as f:
      conn = self.database.conn
      cur = conn.cursor()
      cur.executescript(f.read())
  
  async def on_wavelink_node_ready(self, node: wavelink.Node):
    self.logger.info(f"Wavelink's node {node.id} is ready.")
    
  
  @tasks.loop(minutes=1.0)
  async def update_presence(self) -> None:
    await self.change_presence(
      status=discord.Status.idle,
      activity=discord.Game(
        random.choice(["Created by FlamesCoder ♡", f"Guilds: {len(bot.guilds)}"])
      ),
    )
  
  @update_presence.before_loop
  async def before_update_presence(self) -> None:
    await self.wait_until_ready()
  
  async def load_cogs(self) -> None:
    logger.info("Loading cogs")
    for filename in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
      if filename.endswith(".py"):
        try:
          await self.load_extension(f"cogs.{filename[:-3]}")
          self.logger.info(f"Loaded extension: {filename[:-3]}")
        except Exception as e:
          self.logger.error(
            f'Failed to load extension {filename[:-3]}\n{f"{type(e).__name__}: {e}"}'
          )

load_dotenv()

bot = Bot()

bot.run(os.getenv("TOKEN"), log_handler=None)
