from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Extra, Field


class PatchInfo(BaseModel):
    name: str
    summary: Optional[str]
    reason: Optional[str]


class Spells(BaseModel):
    key: Optional[str]
    name: str
    changes: List[str]


class Champions(PatchInfo):
    base_stats: Optional[List[str]] = None
    spells: Optional[List[Spells]]


class RunesItems(PatchInfo):
    changes: List[str]


class PatchSchema(BaseModel):
    version: str
    creation_date: datetime = Field(default_factory=datetime.now)
    champions: Optional[List[Champions]] = None
    items: Optional[List[RunesItems]] = None
    runes: Optional[List[RunesItems]] = None


class GetPatchSchema(BaseModel):
    id: str

    class Config:
        extra = Extra.allow
