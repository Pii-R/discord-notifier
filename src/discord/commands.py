from abc import ABC, abstractmethod
from typing import Dict

import discord

from .logic import check_command, extract_command_args, extract_command_name


class Command(ABC):
    """Abstract class for commands"""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.prefix = "!"

    @abstractmethod
    def execute(self, message: discord.message.Message):
        """Execute the command logic

        Args:
            message: discord message received
        """
        ...

    def return_command_error(message: discord.message.Message):
        """Return message error

        Args:
            message: discord message received
        """
        ...


class HelpCommand(Command):
    """Help command displaying info on the bot"""

    def __init__(self):
        super().__init__("help", "this is an help command")

    async def execute(self, message: discord.message.Message):
        print(f"{message.author.name}, here's your help")


class SubscribeCommand(Command):
    """Subscribe command allowing user
    to subscribe to notification"""

    def __init__(self):
        super().__init__("subscribe", "this is the subscribe command")

    async def return_command_error(message: discord.message.Message):
        await message.channel.send(f"Error in command, please try again")

    async def execute(self, message: discord.message.Message):
        args = extract_command_args(message.content)
        if len(args) != 1:
            await self.return_command_error()
            return
        summoner_name = extract_command_args(message.content)[0]
        await message.channel.send(
            f"Hi {message.author.name}, you're subscribed with {summoner_name}"
        )


class CommandsHandler:
    """Handler for commands"""

    def __init__(self):
        self.commands: Dict[str, Command] = {}
        self.add_commands([HelpCommand(), SubscribeCommand()])
        self.command_regex = r"^[\!][a-z]*(\s[a-z]*)*"

    def add_commands(self, commands_cls: list[Command]):
        """Add command to the class

        Args:
            name: name of the command
            command_cls: command
        """
        for cmd_cls in commands_cls:
            self.commands[cmd_cls.name] = cmd_cls

    async def handle_command(self, message: discord.message.Message):
        """handle received command

        Args:
            message: message received from user
        """
        if not check_command(message.content, self.command_regex):
            return
        cmd_name = extract_command_name(message.content)

        cmd_cls = self.commands[cmd_name]
        await cmd_cls.execute(message)
