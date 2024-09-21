from typing import Optional, List

from fastapi import HTTPException

from app.core.config import settings
from app.crud import response_creation
from app.db import firebase
from app.schema.item import ItemSchema


class Item:
    def __init__(self, patch_version: str) -> None:
        self.__patch_version: str = patch_version

    @staticmethod
    async def add(item: ItemSchema | dict):
        if isinstance(item, dict):
            item = ItemSchema(**item)

        _item: dict = item.dict()

        check_item = (
            firebase.db.collection(settings.ITEM_COLLECTION)
            .where('patch', '==', item.patch)
            .where('name', '==', item.name)
            .limit(1)
            .stream()
        )
        async for _ in check_item:
            raise HTTPException(
                400,
                f"Item {item.name} with patch version {item.patch} already exists."
            )

        doc_ref = firebase.db.collection(settings.ITEM_COLLECTION).document()
        await doc_ref.set(_item)

        return response_creation(
            f"Item {item.name} with patch version {item.patch} successfully added.",
            doc_ref.id
        )

    async def get(self, fields: Optional[List[str]] = None):
        result: list[dict] = []

        docs = (
            firebase.db.collection(settings.ITEM_COLLECTION)
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
