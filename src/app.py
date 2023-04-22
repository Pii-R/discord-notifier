import time
from datetime import datetime

from src.games.lol.handler import RiotSettings
from src.games.lol.info import SummonerInfo
from src.games.lol.messages import Message
from src.games.lol.regions import Regions
from src.messages.discord.handler import DiscordMessageHandler, DiscordSettings
from src.users.models import User

SUBSCRIBERS = [
    User(
        name="Pierre", discord_id="239145363041157122", lol_summoner_name="EggsKeyScore"
    ),
    User(
        name="Hugo",
        discord_id="173516740993613824",
        lol_summoner_name="Bédé",
    ),
    User(
        name="Lucas",
        discord_id="219539954190123008",
        lol_summoner_name="Vanadium13",
    ),
]


def send_messages():
    riot_settings = RiotSettings(_env_file=".env.test", _env_file_encoding="utf-8")
    discord_settings = DiscordSettings(
        _env_file=".env.test", _env_file_encoding="utf-8"
    )
    handler = DiscordMessageHandler(discord_settings)
    messages = {}
    for subscriber in SUBSCRIBERS:
        if subscriber.discord_id not in messages:
            messages[subscriber.discord_id] = []
        summ_info = SummonerInfo(
            riot_settings, subscriber.lol_region, subscriber.lol_summoner_name
        )
        daily_result = summ_info.get_daily_wins()
        messages[subscriber.discord_id].append(
            Message.format_daily_recap_message(daily_result)
        )
    handler.run(messages)


def main():
    while 1:
        now = datetime.now()
        if (now.hour, now.minute) == (20, 0):
            send_messages()
        time.sleep(30)


if __name__ == "__main__":
    main()
