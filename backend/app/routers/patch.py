from typing import List, Optional

from fastapi import APIRouter, Query

from app.crud.patch import Patch
from app.schema.patch import PatchSchema, GetPatchSchema

router = APIRouter()


@router.post('/patch')
async def create_patch(patch: PatchSchema):
    result = await Patch.add(patch)
    return result


@router.get('/patch', response_model=List[GetPatchSchema])
async def get_all_patch(fields: Optional[List[str]] = Query(None)):
    last_version = await Patch.get_last_version()
    result = await Patch(last_version['version']).get(fields)
    return result


@router.get('/patch/latest', response_model=dict)
async def get_latest_patch():
    result = await Patch.get_last_version()
    return result


@router.get('/patch/{version}', response_model=GetPatchSchema)
async def get_patch(version: str):
    result = await Patch(version).get()
    return result[0]
