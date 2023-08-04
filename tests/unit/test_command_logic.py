"""Tests for command logic"""
from src.discord.logic import (
    check_command,
    extract_command_name_and_args,
    extract_schedule_input,
)


def test_check_command_format():
    """Check if command is formated as expected or not"""
    command = "!test user"
    assert check_command(command, r"^[\!][a-z]*(\s[a-z]*)*")
    false_command = "*test user"
    assert not check_command(false_command, r"^[\!][a-z]*(\s[a-z]*)*")


def test_command_extraction():
    """Test extraction of command name and args"""
    command = "!help"
    assert extract_command_name_and_args(command) == ("help", [])

    command = "!subscribe pierre"
    assert extract_command_name_and_args(command) == ("subscribe", ["pierre"])


def test_extraction_schedule():
    user_input = "!command 1 * 8 8 * *"
    assert extract_schedule_input(user_input, "!") == ("command", 1, "* 8 8 * *")
