import os
import discord
import logging
import platform
from typing import Dict
from HeartSanctifier import HeartSanctifier
from discord.ext import commands

bot_token = os.getenv("DISCORD_TOKEN")
log_level = os.getenv("LOG_LEVEL", logging.NOTSET)
version = os.getenv("VERSION", "development")

"""
https://discordpy.readthedocs.io/en/latest/intents.html
https://discordpy.readthedocs.io/en/latest/intents.html#privileged-intents
"""
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True


class BroLarryBot(commands.Bot):
    def _setupLogger(self, level):
        """
        logging.NOTSET=0
        logging.DEBUG=10
        logging.INFO=20
        logging.WARNING=30
        logging.ERROR=40
        logging.CRITICAL=50
        logging.FATAL=50
        """
        self.logger = logging.getLogger("bro-larry-bot")
        self.logger.setLevel(int(level))
        console_handler = logging.StreamHandler()
        self.logger.addHandler(console_handler)

    def __init__(self, logLevel, verison, *args, **kwargs) -> None:
        super().__init__(command_prefix="!", intents=intents)
        self._setupLogger(logLevel)
        self.version = version
        # Store individual HeartSanctifier instances for each user
        self.user_hearts: Dict[int, HeartSanctifier] = {}

    async def _set_default_avatar(self) -> None:
        """
        Set the bot's avatar to bro_larry.JPG if it exists
        """
        try:
            # Get the directory where the bot.py file is located
            bot_dir = os.path.dirname(os.path.realpath(__file__))
            avatar_path = os.path.join(bot_dir, "bro_larry.JPG")
            
            # Check if the avatar file exists
            if os.path.exists(avatar_path):
                with open(avatar_path, 'rb') as avatar_file:
                    avatar_data = avatar_file.read()
                    await self.user.edit(avatar=avatar_data)
                    self.logger.info("Successfully set bot avatar to bro_larry.JPG")
            else:
                self.logger.warning(f"Avatar file not found at: {avatar_path}")
        except discord.HTTPException as e:
            self.logger.error(f"Failed to set bot avatar due to Discord API error: {e}")
        except Exception as e:
            self.logger.error(f"Failed to set bot avatar: {e}")

    async def load_cogs(self) -> None:
        for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
            if file.endswith(".py"):
                extension = file[:-3]
                try:
                    await self.load_extension(f"cogs.{extension}")
                    self.logger.info(f"Loaded extension '{extension}")
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    self.logger.error(f"Failed to load extension {extension}\n{exception}")

    async def setup_hook(self) -> None:
        """
        Executed the first time the bot starts.
        """
        self.logger.info(f"Logged in as {self.user.name}")
        self.logger.info(f"discord.py API version: {discord.__version__}")
        self.logger.info(f"Python version: {platform.python_version()}")
        self.logger.info(f"bro-larry-bot version {self.version}")
        self.logger.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")
        self.logger.info("-------------------")
        
        # Set the default avatar
        await self._set_default_avatar()
        
        # Load cogs
        await self.load_cogs()

    async def on_command_completion(self, ctx) -> None:
        """
        Executed on successful command
        """
        full_name = ctx.command.qualified_name
        split = full_name.split(" ")
        command = str(split[0])
        self.logger.info(f"Executed {command} command by {ctx.author} ({ctx.author.id})")

    async def on_command_error(self, ctx, err) -> None:
        """
        Executed on error in a command
        """
        full_name = ctx.command.qualified_name
        split = full_name.split(" ")
        command = str(split[0])
        self.logger.warning(f"Error on {command} by {ctx.author} ({ctx.author.id}): {err}")
        if not isinstance(err, commands.CheckFailure):
            await ctx.send('James 3:2 "We all stumble in many ways...", even Bro Larry makes mistakes')


bot = BroLarryBot(log_level, version)
bot.run(bot_token)