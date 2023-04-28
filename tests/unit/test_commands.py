"""Test for commands object"""
import re
from typing import Tuple

import pytest

from src.discord.commands import Command


class HelpCommand(Command):
    """Help command displaying info on the bot"""

    def __init__(self):
        super().__init__("help", "this is an help command")

    async def execute(self, user: str):
        print(f"{user}, here's your help")


class SubscribeCommand(Command):
    """Subscribe command allowing user
    to subscribe to notification"""

    def __init__(self):
        super().__init__("subscribe", "this is the subscribe command")

    async def execute(self, user: str, summoner_name: str):
        print(f"Hi {user}, you're subscribed with {summoner_name}")


def extract_command_args(command_text: str) -> Tuple[str, list[str]]:
    """Extract args and command name from a correct command

    Args:
        command_text (str): text of the correct command

    Returns:
        Tuple[str, list[str]]: command name, list of args of the command
    """
    split_command = command_text.split(" ")
    command = split_command[0].replace("!", "")
    args = command_text.split(" ")[1:]
    return command, args


def check_command(command_text: str) -> bool:
    "check if the command is valid"
    command_re = re.match(r"^[\!][a-z]*(\s[a-z]*)*", command_text)
    return command_re is not None


@pytest.mark.asyncio
async def test_help_command():
    """Test for help commands"""
    help = HelpCommand()
    assert help.prefix == "!"
    await help.execute("pierre")


@pytest.mark.asyncio
async def test_sub_command():
    """Test for help commands"""
    sub = SubscribeCommand()
    assert sub.prefix == "!"
    await sub.execute("pierre", "eggskeyscore")


def test_check_command_format():
    """Check if command is formated as expected or not"""
    command = "!test user"
    assert check_command(command)
    false_command = "*test user"
    assert not check_command(false_command)


def test_command_extraction():
    """Test extraction of command name and args"""
    command = "!help"
    assert extract_command_args(command) == ("help", [])

    command = "!subscribe pierre"
    assert extract_command_args(command) == ("subscribe", ["pierre"])
