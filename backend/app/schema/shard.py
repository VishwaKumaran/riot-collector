from pydantic import BaseModel, Field


class ShardSchema(BaseModel):
    name: str
    patch: str
    icon: str = Field(alias='iconPath')
    description: str = Field(alias='longDesc')
