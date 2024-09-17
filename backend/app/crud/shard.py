from fastapi import HTTPException

from app.core.config import settings
from app.crud import response_creation
from app.db import firebase
from app.schema.shard import ShardSchema


class Shard:
    @staticmethod
    async def add(shard: ShardSchema | dict):
        if isinstance(shard, dict):
            shard = ShardSchema(**shard)

        _shard: dict = shard.dict()

        check_shard = (
            firebase.db.collection(settings.SHARD_COLLECTION)
            .where('patch', '==', shard.patch)
            .where('name', '==', shard.name)
            .limit(1)
            .stream()
        )

        async for _ in check_shard:
            raise HTTPException(
                400,
                f"Shard {shard.name} with patch version {shard.patch} already exists."
            )

        doc_ref = firebase.db.collection(settings.SHARD_COLLECTION).document()
        await doc_ref.set(_shard)

        return response_creation(
            f"Shard {shard.name} with patch version {shard.patch} successfully added.",
            doc_ref.id
        )
