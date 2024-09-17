from typing import List, Optional

from fastapi import APIRouter, Query

from app.crud.item import Item
from app.schema.item import ItemSchema, ItemGetSchema

router = APIRouter()


@router.post('/items')
async def create_items(item: ItemSchema):
    result = await Item.add(item)
    return result


@router.get('/items/{patch_version}', response_model=List[ItemGetSchema])
async def get_items(patch_version: str, fields: Optional[List[str]] = Query(None)):
    result = await Item(patch_version).get(fields)
    return result
