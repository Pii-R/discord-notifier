"""Models for summoners"""

from pydantic import BaseModel, Field


class Summoner(BaseModel):
    id: str
    account_id: str = Field(alias="accountId")
