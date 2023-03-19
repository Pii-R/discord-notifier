from datetime import datetime
from typing import List

from pydantic import BaseSettings, Field
from riotwatcher import LolWatcher

from .summoner import Summoner


class RiotSettings(BaseSettings):
    api_key: str = Field(..., env="RIOT_API_KEY")


class RiotHandler:
    def __init__(self, settings: RiotSettings, region: str):
        self.lolwatcher = LolWatcher(settings.api_key)
        self.region = region

    def get_summoner_by_name(self, summoner_name: str) -> Summoner:
        """Get summoners info by name

        Args:
            region: region of the account
            summoner_name: name of the summoner
        """
        return Summoner(**self.lolwatcher.summoner.by_name(self.region, summoner_name))

    def get_matchlist_by_account(
        self, puuid: str, start_time: datetime, end_time: datetime
    ) -> List[str]:
        """get the macths list from a puuid

        Args:
            puuid: puuid of the player
            start_time: time to start the search
            end_time: time to the end of the search

        Returns:
            return the matchlist of the given puuid
        """
        if start_time and end_time:
            return self.lolwatcher.match.matchlist_by_puuid(
                self.region,
                puuid,
                start_time=int(start_time.timestamp()),
                end_time=int(end_time.timestamp()),
            )
        return self.lolwatcher.match.matchlist_by_puuid(self.region, puuid)

    def get_match_details(self, match_id: str):
        """get the details of a match by its id

        Args:
            match_id : id of the match
        """
        return self.lolwatcher.match.by_id(self.region, match_id)

    def is_match_won_from_puuid_side(self, match_details: dict, puuid: str):
        """determines if a match is won from a the side of a given puuid

        Args:
            match_result:  details of the match
            puuid: puuid of the player
        """
        puiid_details = [
            details
            for details in match_details["info"]["participants"]
            if details["puuid"] == puuid
        ][0]
        return puiid_details["win"]


if __name__ == "__main__":
    settings = RiotSettings(_env_file=".env.test", _env_file_encoding="utf-8")
    handler = RiotHandler(settings, "EUW1")
    summoner = handler.get_summoner_by_name("EggsKeyScore")
    print(summoner)
    # matchs = handler.get_matchlist_by_account(summoner.puuid)
    match = handler.get_match_details("EUW1_6321801583")
    response = handler.is_match_won_from_puuid_side(
        match,
        "cCoJOlgwwoYLv9yUO01A9TDXbzK1kKl9lKSOHwbNPMfMc90nBShzUOFvKBiGkmF8kCoLL5uqn2WoAA",
    )
    print(response)
