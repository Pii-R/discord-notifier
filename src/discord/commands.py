from abc import ABC, abstractmethod
from typing import Dict, List

from tabulate import tabulate

import discord

from ..database.logic import DatabaseOperation
from ..tasks.task import TaskHandler
from .logic import (
    check_command,
    check_valid_timezone,
    extract_command_args,
    extract_command_name,
    extract_schedule_input,
    format_dict_list_to_table_for_discord,
)


class Command(ABC):
    """Abstract class for commands"""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.prefix = "!"
        self.is_changing_task = False

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
        self.is_changing_task = True

    async def return_command_error(self, message: discord.message.Message):
        await message.channel.send(f"Error in command, please try again")

    async def execute(self, message: discord.message.Message):
        adding_user = self.db_handler.add_user(message.author.id, message.author.name)
        self.db_handler.set_notification_time(message.author.id, "0 21 * * *", 1)

        if adding_user:
            await message.channel.send(
                f"Hi {message.author.name}, you're subscribed to the bot"
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
        self.is_changing_task = True


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


class SetTimeCommand(Command):
    """Time command allowing user
    to set time to be notified"""

    def __init__(self, db_handler: DatabaseOperation):
        super().__init__(
            "time", "this is the command to set notification's time to a specific task"
        )
        self.db_handler = db_handler
        self.is_changing_task = True


    async def return_command_error(self, message: discord.message.Message):
        await message.channel.send(
            f"Error in command, you need to specify an id and schedule. Ex: {self.prefix}{self.name} 1 0 * * * *"
        )

    async def execute(self, message: discord.message.Message):
        args = extract_schedule_input(message.content, self.prefix)
        if len(args) != 3:
            await self.return_command_error(message)
            return
        self.db_handler.update_schedule(args[1], args[2])
        await message.channel.send(f"Your subscriptions has been updated")


class StatusCommand(Command):
    """To get status of the bot"""

    def __init__(self):
        super().__init__("status", "this is the status command")

    async def return_command_error(self, message: discord.message.Message):
        await message.channel.send(f"Error in command, please try again")

    async def execute(self, message: discord.message.Message):
        await message.channel.send(f"Hi {message.author.name}, your bot is alive")


class SubscripionsCommand(Command):
    def __init__(self, db_handler: DatabaseOperation):
        super().__init__(
            "subscriptions",
            "this is the subscritpions command to list all susbcritions",
        )
        self.db_handler = db_handler

    async def return_command_error(self, message: discord.message.Message):
        await message.channel.send(f"Error in command, please try again")

    async def execute(self, message: discord.message.Message):
        subscriptions = self.db_handler.get_subscriptions_details(message.author.id)

        format_message = f"You have {len(subscriptions)} subscriptions:\n\n{format_dict_list_to_table_for_discord(subscriptions,headers=["id", "subscription_name", "schedule"])}"
        await message.channel.send(format_message)


class GetTimezoneCommand(Command):
    def __init__(self, db_handler: DatabaseOperation):
        super().__init__("timezone", "Get the current timezone")
        self.db_handler = db_handler

    async def return_command_error(self, message: discord.message.Message):
        await message.channel.send(f"Error in command, please try again")

    async def execute(self, message: discord.message.Message):
        users_timezone = self.db_handler.get_timezone(message.author.id)

        format_message = f"Selected timezone: {users_timezone}"
        await message.channel.send(format_message)


class SetTimezoneCommand(Command):
    def __init__(self, db_handler: DatabaseOperation):
        super().__init__(
            "settimezone",
            "Set the current timezone. Full list here https://en.wikipedia.org/wiki/List_of_tz_database_time_zones",
        )
        self.db_handler = db_handler
        self.is_changing_task = True


    async def return_command_error(self, message: discord.message.Message):
        await message.channel.send(f"Error in command, please try again")

    async def execute(self, message: discord.message.Message):
        args = extract_command_args(message.content)
        if len(args) != 1:
            await self.return_command_error(message)
            return

        timezone = args[0]

        if not check_valid_timezone(timezone):
            await message.channel.send("Given timezone invalid")
            return

        self.db_handler.set_timezone(message.author.id, timezone)

        format_message = f"Selected timezone: {timezone}"
        await message.channel.send(format_message)


class CommandsHandler:
    """Handler for commands"""

    def __init__(
        self,
        commands: List[Dict[str, Command]] | None,
        client: discord.Client,
        db_handler: DatabaseOperation,
    ):
        self.commands = commands if not commands else {}
        self.db_handler = db_handler
        self.add_commands(commands)
        self.command_regex = r"^[\!][a-z_]{1,}"
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

    async def handle_command(self, message: discord.message.Message,task_handler:TaskHandler):
        """handle received command

        Args:
            message: message received from user
        """
        if not check_command(message.content, self.command_regex):
            await self.handle_uncorrect_commands(message)
            return
        cmd_name = extract_command_name(message.content)
        if cmd_name not in self.commands:
            await self.handle_uncorrect_commands(message)
            return
        cmd_cls:Command = self.commands[cmd_name]
        await cmd_cls.execute(message)
        if cmd_cls.is_changing_task:
            await task_handler.start_tasks()

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
