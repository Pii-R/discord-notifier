from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..models.user import Base

engine = create_engine("sqlite:///discord_bot.sqlite")


def session_factory():
    Session = sessionmaker(bind=engine)
    return Session()


def execute_engine():
    Base.metadata.create_all(engine)
