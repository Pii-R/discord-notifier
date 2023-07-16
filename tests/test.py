import unittest
from unittest.mock import AsyncMock, MagicMock

from src.discord.commands import SubscribeCommand


class TestSubscribeCommand(unittest.IsolatedAsyncioTestCase):
    async def test_execute(self):
        message_content = "!subscribe JohnDoe"
        message = MagicMock()
        message.content = message_content
        message.author.name = "TestUser"
        message.channel.send = AsyncMock()

        command = SubscribeCommand()
        await command.execute(message)

        expected_message = f"Hi TestUser, you're subscribed with JohnDoe"
        message.channel.send.assert_called_once_with(expected_message)
