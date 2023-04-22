from pydantic import BaseModel

from src.games.lol.regions import Regions


class User(BaseModel):
    name: str
    discord_id: str
    lol_summoner_name: str
    lol_region: Regions = Regions.EUW1.name
