"""Configuration of the database"""

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker

from .base import Base

prd_engine = create_engine("sqlite:///discord_bot.sqlite")


def session_factory(engine: Engine):
    Session = sessionmaker(bind=engine)
    return Session()


def execute_engine(engine: Engine):
    Base.metadata.create_all(engine, checkfirst=True)


class DatabaseConfiguration:
    def __init__(self, engine: Engine = prd_engine):
        execute_engine(engine)
        self.session = session_factory(engine)
