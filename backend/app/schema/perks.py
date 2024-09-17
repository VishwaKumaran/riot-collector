from typing import List

from pydantic import BaseModel, Field, Extra


class Rune(BaseModel):
    name: str
    icon: str
    short_description: str
    description: str


class Slots(BaseModel):
    name: str
    runes: List[Rune]


class PerksSchema(BaseModel):
    name: str
    icon: str
    keystone: List[Rune]
    slots: List[Slots]
    patch: str


class PerksGetSchema(BaseModel):
    id: str

    class Config:
        extra = Extra.allow
