"""Configuration of the database"""

import csv
from pathlib import Path
from typing import Any, List

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker

from .base import Base
from .models import Notifications, Quotes

QUOTES_PATH = Path(__file__).parent.parent.parent / "quotes.csv"
NOTIFICATIONS_PATH = Path(__file__).parent.parent.parent / "notifications.csv"


def session_factory(engine: Engine):
    Session = sessionmaker(bind=engine)
    return Session()


def execute_engine(engine: Engine):
    Base.metadata.create_all(engine, checkfirst=True)


class DatabaseConfiguration:
    def __init__(self, engine: Engine = None):
        if not engine:
            engine = create_engine("sqlite:///discord_bot.sqlite")
        execute_engine(engine)
        self.session = session_factory(engine)
        self.initialize_table(Quotes, convert_csv_to_dict(QUOTES_PATH))
        self.initialize_table(Notifications, convert_csv_to_dict(NOTIFICATIONS_PATH))

    def initialize_table(self, table: Base, content: dict):
        """initialize a table with a dict

        Args:
            table: table to initialize
            content: content to add to the table
        """
        values_to_add = [table(**rows) for rows in content]
        self.session.add_all(values_to_add)
        self.session.commit()


def convert_csv_to_dict(csv_path: Path, delimiter: str = ",") -> List[dict[str, Any]]:
    """Converts a csv to a dict

    Args:
        csv_path: path of the csv to convert
        delimiter: delimiter of csv

    Returns:
        list of dicts from csv
    """
    with open(csv_path, "r", encoding="utf-8") as csv_file:
        csv_dict = csv.DictReader(csv_file, delimiter=delimiter)
        list_csv = list(csv_dict)

    return list_csv
