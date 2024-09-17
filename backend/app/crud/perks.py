from typing import Optional, List

from fastapi import HTTPException

from app.core.config import settings
from app.crud import response_creation
from app.db import firebase
from app.schema.perks import PerksSchema


class Perks:
    def __init__(self, patch_version: str) -> None:
        self.__patch_version: str = patch_version

    @staticmethod
    async def add(perks: PerksSchema | dict):
        if isinstance(perks, dict):
            perks = PerksSchema(**perks)

        _perks: dict = perks.dict()

        check_perks = (
            firebase.db.collection(settings.PERKS_COLLECTION)
            .where('patch', '==', perks.patch)
            .where('name', '==', perks.name)
            .limit(1)
            .stream()
        )
        async for _ in check_perks:
            raise HTTPException(
                200,
                f"Perks {perks.name} with patch version {perks.patch} already exists."
            )

        doc_ref = firebase.db.collection(settings.PERKS_COLLECTION).document()
        await doc_ref.set(_perks)

        return response_creation(
            f"Perks {perks.name} with patch version {perks.patch} successfully added.",
            doc_ref.id
        )

    async def get(self, fields: Optional[List[str]] = None):
        result: list[dict] = []

        docs = (
            firebase.db.collection(settings.PERKS_COLLECTION)
            .where('patch', '==', self.__patch_version)
        )
        if fields:
            docs = docs.select(fields)

        async for doc in docs.stream():
            _doc = doc.to_dict()
            _doc['id'] = doc.id
            result.append(_doc)

        if not result:
            raise HTTPException(400, f"No data found in patch {self.__patch_version}.")

        return result
