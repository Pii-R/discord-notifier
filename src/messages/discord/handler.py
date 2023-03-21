import os
import discord
from pydantic import BaseSettings, Field


class DiscordSettings(BaseSettings):
    token: str = Field(..., env="DISCORD_TOKEN")


class DiscordMessageClient(discord.Client):
    async def on_ready(self):
        for user_id, messages in self.messages.items():
            user = await self.fetch_user(user_id)
            for message in messages:
                await user.send(message)
        await self.close()

    def update_messages(self, messages: dict):
        """update messages

        Args:
            messages: list of messages for each user
        """
        self.messages = messages


class DiscordMessageHandler:
    def __init__(self, settings: DiscordSettings):
        self.client = DiscordMessageClient(intents=discord.Intents.default())
        self.settings = settings

    def run(self, messages: dict):
        self.client.update_messages(messages)
        self.client.run(self.settings.token)


# messages_to_send = {user1:[message, message1],user2:[message]}
if __name__ == "__main__":
    settings = DiscordSettings(_env_file=".env.test", _env_file_encoding="utf-8")
    handler = DiscordMessageHandler(settings)
    handler.run({"239145363041157122": ["premier message", "seconde message"]})
