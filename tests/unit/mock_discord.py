"""Mock ressources for discord tests"""
from dataclasses import dataclass
from unittest.mock import AsyncMock


@dataclass
class Author:
    id: int
    name: str


class Channel:
    async def send(*args):
        ...


@dataclass
class MockDiscordMessage:
    content: str
    author: Author
    channel: AsyncMock


help_message = MockDiscordMessage("!help", Author(321321, "pierre"), AsyncMock())
sub_message = MockDiscordMessage(
    "!subscribe summoner_name", Author(321321, "pierre"), AsyncMock()
)
