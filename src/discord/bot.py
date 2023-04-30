"""Main logic of the bot"""


from pydantic import BaseSettings, Field

import discord

from ..logger.logger import logger
from .commands import CommandsHandler


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
        self.commands_handler = CommandsHandler(self)

    async def on_ready(self):
        print("Notifier is ready to serve")

    async def on_message(self, message: discord.message.Message):
        """Function triggered when the bot received a message

        Args:
            message: message received by the bot
        """
        logger.debug(f"{message.author.name} in {message.channel}: {message.content}")
        await self.commands_handler.handle_command(message)


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
