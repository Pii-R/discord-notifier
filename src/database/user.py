from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class DiscordUser(Base):
    __tablename__ = "discord_user"

    discord_id = Column(Integer, primary_key=True, autoincrement=False)
    discord_name = Column(String)
    summoner_name = Column(String, nullable=True)
