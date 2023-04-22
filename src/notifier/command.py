# coding:utf-8

"""Command libraries"""

import asyncio

import discord

from ..python_utils.better_abc import ABCMeta, abstract_attribute, abstractmethod
from ..models.user import DiscordUser
from ..models.session import session_factory


session = session_factory()


class Command(metaclass=ABCMeta):
    @abstract_attribute
    def text(self) -> str:
        pass

    @abstract_attribute
    def example(self) -> str:
        pass

    @abstractmethod
    async def execute(self, *args, **kwargs):
        pass


class Subscribe(Command):
    def __init__(self, prefix):
        self.text = f"{prefix}subscribe"
        self.example = f"{self.text} <summoner_name>"

    async def execute(self, message: discord.message.Message, **kwargs):
        if len(message.content.split()):
            summoner_name = message.content.split()[-1]
            # verify if summoner name exists:
            summoner_exists = True

            discord_id_exists_db = session.query(DiscordUser).filter(
                DiscordUser.discord_id == message.author.id
            )
            if discord_id_exists_db.count() != 0:
                await message.channel.send(f"L'utilisateur existe déjà")
                return
            if summoner_exists:
                user = DiscordUser(
                    discord_id=message.author.id,
                    discord_name=message.author.name,
                    summoner_name=summoner_name,
                )
                session.add(user)
                session.commit()
                await message.channel.send(f"Bienvenue !")


class Unsubscribe(Command):
    def __init__(self, prefix):
        self.text = f"{prefix}unsubscribe"
        self.example = self.text

    async def execute(self, message: discord.message.Message, **kwargs):
        if len(message.content.split()):
            # verify if summoner name exists:
            discord_id_exists_db = session.query(DiscordUser).filter(
                DiscordUser.discord_id == message.author.id
            )
            if discord_id_exists_db.count() != 0:
                deletion = session.query(DiscordUser).get(message.author.id)
                session.delete(deletion)
                session.commit()


class Help(Command):
    def __init__(self, prefix):
        self.text = f"{prefix}help"
        self.example = self.text

    async def execute(
        self, message: discord.message.Message, commands: dict[str, Command], **kwargs
    ):
        available_commands = "\n".join([cmd.example for cmd in commands.values()])
        await message.channel.send(
            f"Ceci est un bot permettant de t'envoyer des notifications.\nLes commandes disponibles sont:\n{available_commands}"
        )


if __name__ == "__main__":
    sub = Subscribe(prefix="!")
    print(sub.text)
    asyncio.run(sub.execute())
