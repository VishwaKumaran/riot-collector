from typing import List, Optional

from fastapi import APIRouter, Query

from app.crud.champion import Champion
from app.schema.champion import ChampionCreate, GetChampion, ListChampion

router = APIRouter()


@router.post('/champions')
async def create_champion(champion: ChampionCreate):
    result = await Champion.add(champion)
    return result


@router.get('/champions/list', response_model=List[ListChampion])
async def get_champion_list():
    result = await Champion.get_list_champions()
    return result


@router.get('/champions/{patch_version}', response_model=List[GetChampion])
async def get_champions_by_patch_version(patch_version: str, fields: Optional[List[str]] = Query(None)):
    return [{"id": "ceci"}]
    # result = await Champion(patch_version).get(fields)
    # return result
