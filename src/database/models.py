from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship

from .base import Base


class DiscordUser(Base):
    __tablename__ = "discord_user"

    discord_id = Column(Integer, primary_key=True, autoincrement=False)
    discord_name = Column(String)
    timezone = Column(String, default="Europe/Paris")
    settings = relationship("UserSettings", back_populates="discord")


class UserSettings(Base):
    __tablename__ = "user_settings"

    id: Mapped[int] = Column(Integer, primary_key=True)
    discord_id = Column(Integer, ForeignKey("discord_user.discord_id"))
    notification_id = Column(Integer, ForeignKey("notifications.id"))
    schedule = Column(String)
    discord = relationship("DiscordUser", foreign_keys=[discord_id])
    notifications = relationship("Notifications", foreign_keys=[notification_id])


class Notifications(Base):
    __tablename__ = "notifications"
    id: Mapped[int] = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    settings = relationship("UserSettings", back_populates="notifications")


class Quotes(Base):
    __tablename__ = "quotes"
    id: Mapped[int] = Column(Integer, primary_key=True)
    quote = Column(String)
    author = Column(String, nullable=True)
