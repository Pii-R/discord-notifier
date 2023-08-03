"""Main logic of the bot"""


from pydantic import BaseSettings, Field

import discord

from ..database.logic import DatabaseConfiguration, DatabaseOperation
from ..logger.logger import logger
from ..tasks.task import TaskHandler
from .commands import CommandsHandler
from .notifier import prepare_tasks


class DiscordSettings(BaseSettings):
    token: str = Field(..., env="DISCORD_TOKEN")


class DiscordClient(discord.Client):
    def __init__(
        self,
        intents: discord.Client.intents,
    ):
        super().__init__(
            intents=intents,
            log_handler=None,
        )

        self.db_handler = DatabaseOperation(DatabaseConfiguration())
        self.commands_handler = CommandsHandler(self, self.db_handler)
        self.tasks_handler = TaskHandler(self, self.db_handler)

    async def on_ready(self):
        print("Notifier is ready to serve")
        # self.tasks = await prepare_tasks(self.db_handler, self)
        await self.tasks_handler.start_tasks()

    async def on_message(self, message: discord.message.Message):
        """Function triggered when the bot received a message

        Args:
            message: message received by the bot
        """

        logger.debug(f"{message.author.name} in {message.channel}: {message.content}")
        if not message.author.bot:
            await self.commands_handler.handle_command(message)
            await self.tasks_handler.start_tasks()


class DiscordBot:
    def __init__(self, settings: DiscordSettings):
        self.client = DiscordClient(intents=discord.Intents.default())
        self.settings = settings

    def run(self):
        self.client.run(self.settings.token)


if __name__ == "__main__":
    settings = DiscordSettings(_env_file=".env.test", _env_file_encoding="utf-8")
    bot = DiscordBot(settings)
    bot.run()
