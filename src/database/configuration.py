"""Configuration of the database"""

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker

from .base import Base
from .models import Citations


def session_factory(engine: Engine):
    Session = sessionmaker(bind=engine)
    return Session()


CITATIONS_INIT = [
    {"text": "Brebis qui bêle, perd sa gueulée."},
    {"text": "Quand la poire est mûre, il faut qu'elle tombe."},
    {
        "text": "Ne crains pas l'année bissextile mais plutôt celle d'avant et celle d'après."
    },
    {"text": "Qui croit venger sa honte l'accroît."},
]


def execute_engine(engine: Engine):
    Base.metadata.create_all(engine, checkfirst=True)


class DatabaseConfiguration:
    def __init__(self, engine: Engine = None):
        if not engine:
            engine = create_engine("sqlite:///discord_bot.sqlite")
        execute_engine(engine)
        self.session = session_factory(engine)
        self.initialize_table(Citations, CITATIONS_INIT)

    def initialize_table(self, table: Base, content: dict):
        """initialize a table with a dict

        Args:
            table: table to initialize
            content: content to add to the table
        """
        values_to_add = [table(**rows) for rows in content]
        self.session.add_all(values_to_add)
        self.session.commit()
