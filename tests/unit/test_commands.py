"""Test for commands object"""

import pytest

from src.discord.commands import CommandsHandler, HelpCommand, SubscribeCommand

from .mock_discord import help_message, sub_message


@pytest.mark.asyncio
async def test_help_command():
    """Test for help commands"""
    help = HelpCommand()
    assert help.prefix == "!"
    await help.execute(help_message)


@pytest.mark.asyncio
async def test_sub_command():
    """Test for help commands"""
    sub = SubscribeCommand()
    assert sub.prefix == "!"
    await sub.execute(sub_message)
    expected_message = (
        f"Hi {sub_message.author.name}, you're subscribed with summoner_name"
    )
    sub_message.channel.send.assert_called_once_with(expected_message)


@pytest.mark.asyncio
async def test_init_commands_handler():
    """Check correct initialization of the commands handler"""
    cmds_handler = CommandsHandler()
    assert len(cmds_handler.commands) == 2

    await cmds_handler.handle_command(help_message)
