"""lolhandler test"""
from unittest.mock import patch

from src.games.lol.handler import RiotHandler, RiotSettings


@patch(
    "src.games.lol.handler.LolWatcher",
)
def test_riothandler(mock):
    """test of get summoner by name method"""
    settings = RiotSettings(_env_file=".env.test", _env_file_encoding="utf-8")
    mock_summoner = {
        "id": "eqewq",
        "accountId": "toto_account",
    }
    mock.return_value.summoner.by_name.return_value = mock_summoner
    handler = RiotHandler(settings)

    summoner = handler.get_summoner_by_name("EUW1", "toto")

    assert summoner.account_id == mock_summoner["accountId"]
    assert summoner.id == mock_summoner["id"]
