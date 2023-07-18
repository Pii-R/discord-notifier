"""Logic for database manipulation"""
import random
from typing import List

from .configuration import DatabaseConfiguration
from .models import DiscordUser, Quotes


class DatabaseOperation:
    def __init__(self, configuration: DatabaseConfiguration):
        self.configuration = configuration
        self.session = self.configuration.session

    def add_user(self, discord_id: int, discord_name: str) -> bool:
        """Add user with summoner name in the database

        Args:
            summoner_name: summoner name from Riot
            discord_id: discord id
        """
        discord_id_exists_db = self.session.query(DiscordUser).filter(
            DiscordUser.discord_id == discord_id
        )
        if discord_id_exists_db.count() != 0:
            return False
        user = DiscordUser(
            discord_id=discord_id,
            discord_name=discord_name,
        )
        self.session.add(user)
        self.session.commit()
        return True

    def remove_user(self, discord_id: int) -> bool:
        """Add user with summoner name in the database

        Args:
            summoner_name: summoner name from Riot
            discord_id: discord id
        """
        discord_id_exists_db = self.session.query(DiscordUser).filter(
            DiscordUser.discord_id == discord_id
        )
        if discord_id_exists_db.count() == 0:
            return False

        if discord_id_exists_db.count() != 0:
            deletion = self.session.query(DiscordUser).get(discord_id)
            self.session.delete(deletion)
            self.session.commit()
            return True

    def get_all_subscribed_user(self) -> List[int]:
        """Retrieve all subscribed users

        Returns:
            List of users' discord id
        """
        return [
            result.discord_id
            for result in self.session.query(DiscordUser.discord_id).all()
        ]

    def get_random_quote(self) -> str:
        """get a random quote from Quotes table

        Returns:
            the chosen quote
        """

        rand = random.randrange(0, self.session.query(Quotes).count())
        row = self.session.query(Quotes)[rand]
        return row.quote
