"""Configuration module for discord bot"""

from pydantic import BaseSettings, Field


class Configuration(BaseSettings):
    token: str = Field(..., env="DISCORD_TOKEN")
