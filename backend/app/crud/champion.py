from typing import List, Optional

from fastapi import HTTPException

from app.core.config import settings
from app.crud import response_creation
from app.crud.patch import Patch
from app.db import firebase
from app.schema.champion import ChampionCreate, GetChampion


class Champion:
    def __init__(self, patch_version: str) -> None:
        self.patch_version: str = patch_version

    @staticmethod
    async def add(champion: ChampionCreate | dict):
        if isinstance(champion, dict):
            champion = ChampionCreate(**champion)

        _champion: dict = champion.dict()

        check_champ = (
            firebase.db.collection(settings.CHAMPION_COLLECTION)
            .where('patch', '==', champion.patch)
            .where('champ_id', '==', champion.champ_id)
            .limit(1)
            .stream()
        )
        async for _ in check_champ:
            raise HTTPException(
                400,
                f'Champion {champion.champ_id} with patch version {champion.patch} already exists.'
            )

        doc_ref = firebase.db.collection(settings.CHAMPION_COLLECTION).document()
        await doc_ref.set(_champion)

        return response_creation(
            f"Champion {champion.champ_id} with patch version {champion.patch} successfully added.",
            doc_ref.id
        )

    @staticmethod
    async def get_list_champions() -> List[dict]:
        result: List[dict] = []
        last_patch_version = await Patch.get_last_version()

        docs = (
            firebase.db.collection(settings.CHAMPION_COLLECTION)
            .where('patch', '==', last_patch_version['version'])
            .select(['name', 'champ_id'])
            .stream()
        )

        async for doc in docs:
            _doc = doc.to_dict()
            _doc['id'] = doc.id
            result.append(_doc)

        return result

    async def get(self, fields: Optional[List[str]] = None) -> List[GetChampion]:
        result: List[GetChampion] = []

        docs = (
            firebase.db.collection(settings.CHAMPION_COLLECTION)
            .where('patch', '==', self.patch_version)
        )
        if fields:
            docs = docs.select(fields)

        async for doc in docs.stream():
            _doc = doc.to_dict()
            _doc['id'] = doc.id
            result.append(_doc)

        if not result:
            raise HTTPException(400, f"No data found in patch {self.patch_version}.")

        return result
