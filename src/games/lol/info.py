"""Info module"""
from .handler import RiotHandler, RiotSettings
from .summoner import Summoner
from datetime import datetime


class SummonerInfo:
    def __init__(self, settings: RiotSettings, region: str, summoner_name: str):
        self.riothandler = RiotHandler(settings, region)
        self.summoner = self.riothandler.get_summoner_by_name(summoner_name)

    def get_daily_wins(self) -> dict[str, str]:
        """Get daily wins"""
        now = datetime.now()
        start_time = now.replace(hour=0, minute=0, second=0)
        end_time = now.replace(hour=23, minute=59, second=59)
        matchslist = self.riothandler.get_matchlist_by_account(
            self.summoner.puuid, start_time, end_time
        )
        matchsdetails_list = [
            self.riothandler.get_match_details(match_id) for match_id in matchslist
        ]
        wins = len(
            [
                self.riothandler.is_match_won_from_puuid_side(
                    match_details, self.summoner.puuid
                )
                for match_details in matchsdetails_list
                if self.riothandler.is_match_won_from_puuid_side(
                    match_details, self.summoner.puuid
                )
            ]
        )
        return {"wins": wins, "lost": len(matchslist) - wins, "total": len(matchslist)}


if __name__ == "__main__":
    settings = RiotSettings(_env_file=".env.test", _env_file_encoding="utf-8")
    suminfo = SummonerInfo(settings, "EUW1", "EggsKeyScore")
    print(suminfo.get_daily_wins())
