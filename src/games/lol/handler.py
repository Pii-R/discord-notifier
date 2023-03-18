from pydantic import BaseSettings, Field
from requests import Response
from riotwatcher import LolWatcher

from .summoner import Summoner


class RiotSettings(BaseSettings):
    api_key: str = Field(..., env="RIOT_API_KEY")


class RiotHandler:
    def __init__(self, settings: RiotSettings):
        self.watcher = LolWatcher(settings.api_key)

    def get_summoner_by_name(self, region: str, summoner_name: str) -> Summoner:
        """Get summoners info by name

        Args:
            region (str): _description_
            summoner_name (str): _description_
        """
        return Summoner(**self.watcher.summoner.by_name(region, summoner_name))
