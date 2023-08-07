"""Logic for database manipulation"""
import random
from typing import List, Tuple

from .base import Base
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

    def get_all_subscribed_users_to_task(self, task_id: int) -> List[Tuple[int, str]]:
        """Return all subscribed users to a given task

        Args:
            task_id: given task id

        Returns:
            list of given user susbscribed to the given task
        """
        return [
            (result.discord_id, result.schedule)
            for result in self.session.query(UserSettings)
            .filter(UserSettings.notification_id == task_id)
            .all()
        ]

    def get_random_quote(self) -> str:
        """get a random quote from Quotes table

        Returns:
            the chosen quote
        """

        rand = random.randrange(0, self.session.query(Quotes).count())
        row = self.session.query(Quotes)[rand]
        return row.quote

    def insert_rows_to_table(self, table: Base, content: dict):
        """insert dict into table

        Args:
            table: table to update
            content: content to add
        """
        new_rows = []

        # Check if the rows already exist and filter out duplicates
        for data in content:
            row_exists = self.session.query(table).filter_by(**data).first()
            if not row_exists:
                new_row = table(**data)
                new_rows.append(new_row)
            self.session.add_all(new_rows)
            self.session.commit()

    def get_subscriptions_details(self, user_id: int) -> List[dict]:
        """return all susbcriptions from a user id

        Args:
            user_id: user id

        Returns:
            the detailed list of the user's subscriptions
        """
        query = (
            self.session.query(
                UserSettings.id,
                Notifications.name,
                UserSettings.schedule,
            )
            .join(DiscordUser, UserSettings.discord_id == DiscordUser.discord_id)
            .join(Notifications, UserSettings.notification_id == Notifications.id)
        )

        results = query.filter(UserSettings.discord_id == user_id).all()
        return [
            {
                "id": subscriptions_id,
                "subscription_name": notification_name,
                "schedule": schedule,
            }
            for subscriptions_id, notification_name, schedule in results
        ]

    def update_schedule(self, subscription_id: int, new_schedule: str):
        """Update schedule of the given subscription id

        Args:
            subscription_id: id of the subscription
        """
        user_settings = (
            self.session.query(UserSettings).filter_by(id=subscription_id).first()
        )

        if user_settings:
            # Update the schedule field
            user_settings.schedule = new_schedule

            # Commit the changes to the database
            self.session.commit()

    def get_timezone(self, user_id: str) -> str:
        """Returns the current timezone of the given user

        Args:
            user_id: id of the user

        Returns:
            timezone of the user
        """
        users_timezone = (
            self.session.query(DiscordUser.timezone)
            .filter_by(discord_id=user_id)
            .first()
        )

        return users_timezone[0]

    def set_timezone(self, user_id: str, timezone: str):
        """Set the timezone for the given user

        Args:
            user_id: id of the user
            timezone: timezone to add

        """
        user = (
            self.session.query(DiscordUser)
            .filter(DiscordUser.discord_id == user_id)
            .first()
        )

        if not user:
            return False

        user.timezone = timezone
        self.session.commit()

        return True
