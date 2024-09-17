from typing import List, Optional

from fastapi import HTTPException

from app.core.config import settings
from app.crud import response_creation
from app.db import firebase
from app.schema.patch import PatchSchema


class Patch:
    def __init__(self, versions: list | str):
        self.versions = [versions] if isinstance(versions, str) else versions

    @staticmethod
    async def add(patch: PatchSchema | dict):
        if isinstance(patch, dict):
            patch = PatchSchema(**patch)

        _patch: dict = patch.dict()

        check_patch = (
            firebase.db.collection(settings.PATCH_COLLECTION)
            .where('version', '==', patch.version)
            .limit(1)
            .stream()
        )
        async for _ in check_patch:
            raise HTTPException(400, f"Patch version {patch.version} already exists.")

        doc_ref = firebase.db.collection(settings.PATCH_COLLECTION).document()
        await doc_ref.set(_patch)

        return response_creation(
            f"Patch version {patch.version} successfully added.",
            doc_ref.id
        )

    @staticmethod
    async def get_last_version() -> dict:
        docs = (
            firebase.db.collection(settings.PATCH_COLLECTION)
            .order_by('creation_date', direction='DESCENDING')
            .limit(1)
            .select(['version'])
            .stream()
        )

        async for doc in docs:
            return {
                "id": doc.id,
                "version": doc.get('version')
            }

    async def get(self, fields: Optional[List[str]] = None) -> List[dict]:
        result: list[dict] = []

        docs = (
            firebase.db.collection(settings.PATCH_COLLECTION)
            .where('version', 'in', self.versions)
        )
        if fields:
            docs = docs.select(fields)

        async for document in docs.stream():
            _doc = document.to_dict()
            _doc["id"] = document.id
            result.append(_doc)

        if not result:
            raise HTTPException(400, f"Patch {', '.join(self.versions)} does not exists.")

        return result
