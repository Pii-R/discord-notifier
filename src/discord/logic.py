"""Logic behind commands handling"""
import re
from typing import List, Tuple

import pytz
from tabulate import tabulate


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


def format_dict_list_to_table_for_discord(data_list):
    """Format a list of dict into a pretty table to send via discord

    Args:
        data_list: list of dict to format

    Returns:
       formated string
    """
    if not data_list or not isinstance(data_list, list):
        return "Input data must be a non-empty list of dictionaries."

    headers = data_list[0].keys()
    rows = [list(item.values()) for item in data_list]

    table = tabulate(rows, headers=headers, tablefmt="rounded_outline")
    return "```\n" + table + "\n```"


def extract_schedule_input(text: str, prefix: str):
    # Extracting the subscription ID and cron expression from the command
    pattern = (
        rf"^\{prefix}"
        + r"([a-z]+)\s(\d+)\s+((?:\*|\d+)\s+(?:\*|\d+)\s+(?:\*|\d+)\s+(?:\*|\d+)\s+(?:\*|\d+))$"
    )
    match = re.match(pattern, text)
    if match:
        command = match.group(1)
        subscription_id = int(match.group(2))
        cron_expression = match.group(3)
        return command, subscription_id, cron_expression
    else:
        return None, None


def check_valid_timezone(timezone_to_check: str) -> bool:
    """Check if given string match a valid timezone

    Args:
        timezone_to_check: timezone to check

    Returns:
        True, if valid timezone. Else False
    """
    return timezone_to_check in pytz.common_timezones
