from typing import List

from pydantic import BaseSettings, Field

import discord

from .command import Command, Help, Subscribe
from .logger import logger


class DiscordSettings(BaseSettings):
    token: str = Field(..., env="DISCORD_TOKEN")


class DiscordClient(discord.Client):
    def __init__(
        self,
        intents: discord.Client.intents,
        commands: List[Command],
        prefix: str,
    ):
        super().__init__(
            intents=intents,
            log_handler=None,
        )
        self.prefix = prefix
        self.commands = {
            cmd(prefix=prefix).text: cmd(prefix=prefix) for cmd in commands
        }

    async def on_ready(self):
        print("Bot's ready")

    async def on_message(self, message: discord.message.Message):
        await self.process_message(self, message)

    async def process_message(
        self, client: discord.Client, message: discord.message.Message
    ):
        if (
            isinstance(message.channel, discord.DMChannel)
            and message.author != client.user
        ):
            logger.debug(
                f"{message.author.name} in {message.channel}: {message.content}"
            )
            possible_sent_command = message.content.split(" ")[0]
            context = {"message": message, "commands": self.commands}

            if message.content.split(" ")[0] in self.commands:
                await self.commands[possible_sent_command].execute(**context)

            elif any(cmd in message.content for cmd in self.commands):
                await message.channel.send(
                    f"Command syntax: {self.prefix}command <arg>"
                )

            else:
                await message.channel.send(
                    f"I'm waiting for a command. See {self.prefix}help"
                )


class DiscordMessageHandler:
    def __init__(self, settings: DiscordSettings, commands: List[Command], prefix: str):
        self.client = DiscordClient(
            intents=discord.Intents.default(),
            commands=commands,
            prefix=prefix,
        )
        self.settings = settings

    def run(self):
        self.client.run(self.settings.token)


# messages_to_send = {user1:[message, message1],user2:[message]}
if __name__ == "__main__":
    settings = DiscordSettings(_env_file=".env.test", _env_file_encoding="utf-8")
    handler = DiscordMessageHandler(settings, commands=[Help, Subscribe], prefix="!")
    handler.run()
