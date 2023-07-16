from abc import ABC, abstractmethod
from typing import Dict

import discord

from ..database.logic import DatabaseConfiguration, DatabaseOperation
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

    def __init__(self, available_commands: dict[str, Command] = None):
        super().__init__("help", "this is an help command")
        self.available_commands = available_commands

    async def execute(self, message: discord.message.Message):
        available_commands_format = (
            ", ".join(cmd.name for cmd in self.available_commands.values())
            if self.available_commands
            else "no commands available"
        )
        await message.channel.send(
            f"{message.author.name}, here's the list of available commands: {available_commands_format}"
        )

    def update_commands_list(self, commands_list: dict[str, Command]):
        """Update the available commands

        Args:
            commands_list: list of updated commands
        """
        self.available_commands = commands_list


class SubscribeCommand(Command):
    """Subscribe command allowing user
    to subscribe to notification"""

    def __init__(self, db_handler: DatabaseOperation):
        super().__init__("subscribe", "this is the subscribe command")
        self.db_handler = db_handler

    async def return_command_error(self, message: discord.message.Message):
        await message.channel.send(f"Error in command, please try again")

    async def execute(self, message: discord.message.Message):
        args = extract_command_args(message.content)
        if len(args) != 1:
            await self.return_command_error(message)
            return
        summoner_name = extract_command_args(message.content)[0]

        adding_user = self.db_handler.add_user_with_summoner_name(
            summoner_name, message.author.id, message.author.name
        )
        if adding_user:
            await message.channel.send(
                f"Hi {message.author.name}, you're subscribed with {summoner_name}"
            )
            return
        await message.channel.send(
            f"Hi {message.author.name}, this user is aldready defined"
        )


class UnsubscribeCommand(Command):
    """Unsubscribe command allowing user
    to unsubscribe to notification"""

    def __init__(self, db_handler: DatabaseOperation):
        super().__init__("unsubscribe", "this is the unsubscribe command")
        self.db_handler = db_handler

    async def return_command_error(self, message: discord.message.Message):
        await message.channel.send(f"Error in command, please try again")

    async def execute(self, message: discord.message.Message):
        removing_user = self.db_handler.remove_user(message.author.id)

        if removing_user:
            await message.channel.send(
                f"Hi {message.author.name}, you've been unsubscribed"
            )
            return
        await message.channel.send(f"Hi {message.author.name}, you were not subscribed")


class TimeCommand(Command):
    """Time command allowing user
    to set time to be notified"""

    def __init__(self, db_handler: DatabaseOperation):
        super().__init__("time", "this is the time command")
        self.db_handler = db_handler

    async def return_command_error(self, message: discord.message.Message):
        await message.channel.send(f"Error in command, please try again")

    async def execute(self, message: discord.message.Message):
        pass


class CommandsHandler:
    """Handler for commands"""

    def __init__(self, client: discord.Client, db_handler: DatabaseOperation = None):
        self.commands: Dict[str, Command] = {}
        if not db_handler:
            db_handler = DatabaseOperation(DatabaseConfiguration())

        self.add_commands(
            [
                HelpCommand(),
                SubscribeCommand(db_handler),
                UnsubscribeCommand(db_handler),
            ]
        )
        self.command_regex = r"^[\!][a-z]*(\s[a-z]*)*"
        self.client = client

    def add_commands(self, commands_cls: list[Command]):
        """Add intanciated commands to the class

        Args:
            name: name of the command
            command_cls: command
        """
        for cmd_cls in commands_cls:
            self.commands[cmd_cls.name] = cmd_cls
        if "help" in self.commands:
            help_cmd: HelpCommand = self.commands["help"]
            help_cmd.update_commands_list(self.commands)

    async def handle_command(self, message: discord.message.Message):
        """handle received command

        Args:
            message: message received from user
        """
        if not check_command(message.content, self.command_regex):
            await self.handle_uncorrect_commands(message)
            return
        cmd_name = extract_command_name(message.content)

        cmd_cls = self.commands[cmd_name]
        await cmd_cls.execute(message)

    async def handle_uncorrect_commands(self, message: discord.message.Message):
        """Function triggered when an unrecognized command is received

        Args:
            message: message received
        """
        if (
            isinstance(message.channel, discord.DMChannel)
            and message.author != self.client.user
        ):
            await message.channel.send(f"Unrecognized command")
