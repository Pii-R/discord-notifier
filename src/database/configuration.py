"""Configuration of the database"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .user import Base

engine = create_engine("sqlite:///discord_bot.sqlite")


def session_factory():
    Session = sessionmaker(bind=engine)
    return Session()


def execute_engine():
    Base.metadata.create_all(engine)


class DatabaseConfiguration:
    def __init__(self):
        execute_engine()
        self.session = session_factory()
