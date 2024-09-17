from fastapi import APIRouter

from app.crud.shard import Shard
from app.schema.shard import ShardSchema

router = APIRouter()


@router.post('/shards')
async def create_shards(shard: ShardSchema):
    result = await Shard.add(shard)
    return result
