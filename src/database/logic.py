"""Logic for database manipulation"""
import random
from datetime import datetime
from typing import List

from .configuration import DatabaseConfiguration
from .models import DiscordUser, Notifications, Quotes, UserSettings


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

    def set_notification_time(
        self, discord_id: int, schedule: str, notification_id: int
    ) -> bool:
        """Set notification time to a user

        Args:
            discord_id: discord if of the user
            time: time to set for notification
        """
        settings_already_exists = self.session.query(UserSettings).filter(
            UserSettings.discord_id == discord_id,
            UserSettings.notification_id == notification_id,
        )
        if settings_already_exists.count() != 0:
            return False

        user_settings = UserSettings(
            discord_id=discord_id, notification_id=notification_id, schedule=schedule
        )
        self.session.add(user_settings)
        self.session.commit()

        return True

    def add_notification(self, name: str, description: str):
        """Add a notification

        Args:
            description: description of the notification
        """
        notification_already_exists = self.session.query(Notifications).filter(
            Notifications.name == name,
            Notifications.description == description,
        )
        if notification_already_exists.count() != 0:
            return False

        notification = Notifications(name=name, description=description)
        self.session.add(notification)
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
