from typing import List, Optional

from pydantic import BaseModel, Field


class SummonerSpellSchema(BaseModel):
    name: str
    description: str
    icon: Optional[str] = Field(alias='iconPath')
    summoner_level: int = Field(alias='summonerLevel')
    cooldown: float
    patch: str
    game_modes: List[str] = Field(alias='gameModes')
