import os
import discord
from pydantic import BaseSettings, Field


class DiscordSettings(BaseSettings):
    token: str = Field(..., env="DISCORD_TOKEN")


class DiscordClient(discord.Client):
    async def on_message(self, message):
        print(f"Message from {message.author}: {message.content}")

    async def on_ready(self):
        user_id = (
            "3312312"  # Replace with the user ID you want to send a direct message to
        )
        user = await self.fetch_user(user_id)
        await user.send("Hello, this is a direct message!")


class DiscordHandler:
    def __init__(self, settings: DiscordSettings):
        self.client = DiscordClient(intents=discord.Intents.default())
        self.settings = settings

    def run(self):
        self.client.run(self.settings.token)


# @client.event
# async def on_ready(self):
#     user_id = "239145363041157122"  # Replace with the user ID you want to send a direct message to
#     user = await self.client.fetch_user(user_id)
#     dm_channel = await user.create_dm()
#     message = "Hello, this is a direct message!"
#     await dm_channel.send(message)
#     await self.client.close()


# client.run("MTA4Njk3MjMyMDYxMjA5NDAwMQ.GsboR-.I4O-a9duSi4Wm6omMsZZQhE7djFXKRZl35_V8M")

# messages_to_send = {user1:[message, message1],user2:[message]}
if __name__ == "__main__":
    settings = DiscordSettings(_env_file=".env.test", _env_file_encoding="utf-8")
    handler = DiscordHandler(settings)
    handler.run()
