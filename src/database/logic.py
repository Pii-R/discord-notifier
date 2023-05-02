"""Logic for database manipulation"""
from .configuration import DatabaseConfiguration
from .models import DiscordUser


class DatabaseOperation:
    def __init__(self, configuration: DatabaseConfiguration):
        self.configuration = configuration
        self.session = self.configuration.session

    def add_user_with_summoner_name(
        self, summoner_name: str, discord_id: int, discord_name: str
    ) -> bool:
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
            summoner_name=summoner_name,
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
