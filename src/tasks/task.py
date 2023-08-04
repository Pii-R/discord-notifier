import asyncio
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, List

import discord

from ..database.logic import DatabaseOperation
from ..database.models import Notifications
from .utils import cron_to_datetime


class Task(ABC):
    """Abstract class for tasks"""

    _subclasses_ids = {}
    _current_id = 0

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.id = Task.generate_id()

    @classmethod
    def generate_id(cls):
        cls._current_id += 1
        cls._subclasses_ids[cls.__name__] = cls._current_id
        return cls._current_id

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is not None:
            raise Exception(f"{cls.__name__} can only be instantiated once.")
        cls._instance = super(Task, cls).__new__(cls)
        return cls._instance

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.subtasks = {}

    @abstractmethod
    def prepare_tasks(self):
        ...


class InspiringQuoteTask(Task):
    def __init__(self, db_handler: DatabaseOperation, client: discord.Client):
        super().__init__(
            name="inspiring quote task", description="send inspiring quote"
        )
        self.db_handler = db_handler
        self.client = client

    async def prepare_tasks(
        self,
    ):
        users_schedule = self.db_handler.get_all_subscribed_users_to_task(self.id)
        for task in self.subtasks.values():
            task.cancel()
        for detail in users_schedule:
            cron = detail[1]

            self.subtasks[detail[0]] = asyncio.create_task(
                self.send_personnalized_message(detail[0], cron)
            )
        await asyncio.gather(*self.subtasks.values())
        return self.subtasks

    def create_message_of_random_quote(self) -> str:
        """Create a message with a random quote from a database

        Args:
            db_handler: database handler where quotes are stored

        Returns:
            the formatted message with the quote
        """
        quote = self.db_handler.get_random_quote()
        return f"Your inspiring quote of the day:\n{quote}"

    async def send_personnalized_message(self, user_id: int, cron: str):
        # Wait until the scheduled time
        while 1:
            current_time = datetime.now()
            target_time = cron_to_datetime(cron)
            # Calculate the time difference to the target time
            time_diff = (target_time - current_time).total_seconds()
            print(target_time, time_diff)
            # If the target time has already passed, schedule the message for the next day
            if time_diff <= 0:
                target_time += datetime.timedelta(days=1)
                time_diff = (target_time - current_time).total_seconds()

            # Wait until the target time is reached
            await asyncio.sleep(time_diff)

            message = self.create_message_of_random_quote()
            user = await self.client.fetch_user(int(user_id))
            # Send the message to the user
            await user.send(message)
            print(f"sent to {user_id}")


class TaskHandler:
    """Handler for tasks"""

    def __init__(
        self,
        client: discord.Client,
        db_handler: DatabaseOperation,
        default_tasks: List[Task] | None = None,
    ):
        self.client = client
        self.db_handler = db_handler
        self.tasks = [InspiringQuoteTask(self.db_handler, self.client)]
        if default_tasks:
            self.tasks += default_tasks
        self.db_handler.insert_rows_to_table(Notifications, self.get_tasks_details())

    def get_tasks_details(self) -> List[dict[str, Any]]:
        return [
            {"id": task.id, "name": task.name, "description": task.description}
            for task in self.tasks
        ]

    async def start_tasks(self):
        for task in self.tasks:
            await task.prepare_tasks()
