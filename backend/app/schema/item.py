from typing import List, Optional

from pydantic import BaseModel, Extra


class StatsValue(BaseModel):
    flat: float
    percent: float


class Stats(BaseModel):
    move_speed: StatsValue
    health: StatsValue
    crit: StatsValue
    magic_damage: StatsValue
    mana: StatsValue
    armor: StatsValue
    magic_resistance: StatsValue
    attack_damage: StatsValue
    attack_speed: StatsValue
    life_steal: StatsValue
    health_regen: StatsValue


class Gold(BaseModel):
    base: int
    purchasable: bool
    total: int
    sell: int


class ItemSchema(BaseModel):
    item_id: int
    patch: str
    name: str
    description: str
    icon: Optional[str]
    build_from: Optional[List[int]]
    build_into: Optional[List[int]]
    tags: List[str]
    max_stacks: Optional[int]
    gold: Gold
    stats: Stats


class ItemGetSchema(BaseModel):
    id: str

    class Config:
        extra = Extra.allow
