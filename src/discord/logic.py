"""Logic behind commands handling"""
import re
from typing import Tuple


def extract_command_name_and_args(command_text: str) -> Tuple[str, list[str]]:
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


def extract_command_name(command_text: str) -> str:
    """Extract command name from a correct command

    Args:
        command_text (str): text of the correct command

    Returns:
        command name
    """
    split_command = command_text.split(" ")
    command = split_command[0].replace("!", "")
    return command


def extract_command_args(command_text: str) -> str:
    """Extract command name from a correct command

    Args:
        command_text (str): text of the correct command

    Returns:
        command args
    """
    args = command_text.split(" ")[1:]
    return args


def check_command(command_text: str, command_regex: str) -> bool:
    """Checl if a command is valid based on a regex

    Args:
        command_text: text of the command
        command_regex: regex to match

    Returns:
        true if command is correct else false
    """
    command_re = re.match(command_regex, command_text)
    return command_re is not None
