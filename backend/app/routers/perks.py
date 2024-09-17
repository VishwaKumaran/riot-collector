from typing import List, Optional

from fastapi import APIRouter, Query

from app.crud.perks import Perks
from app.schema.perks import PerksSchema, PerksGetSchema

router = APIRouter()


@router.post('/perks')
async def create_perks(perks: PerksSchema):
    result = await Perks.add(perks)
    return result


@router.get('/perks/{patch_version}', response_model=List[PerksGetSchema])
async def get_perks(patch_version: str, fields: Optional[List[str]] = Query(None)):
    result = await Perks(patch_version).get(fields)
    return result
