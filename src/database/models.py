from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship

from .base import Base


class DiscordUser(Base):
    __tablename__ = "discord_user"

    discord_id = Column(Integer, primary_key=True, autoincrement=False)
    discord_name = Column(String)
    settings = relationship("UserSettings", back_populates="discord")


class UserSettings(Base):
    __tablename__ = "user_settings"

    id: Mapped[int] = Column(Integer, primary_key=True)
    discord_id = Column(Integer, ForeignKey("discord_user.discord_id"))
    notification_id = Column(Integer, ForeignKey("notifications.id"))
    schedule = Column(String)
    discord = relationship("DiscordUser", back_populates="settings")
    notifications = relationship("Notifications", back_populates="settings")


class Notifications(Base):
    __tablename__ = "notifications"
    id: Mapped[int] = Column(Integer, primary_key=True)
    description = Column(String)
    settings = relationship("UserSettings", back_populates="notifications")
