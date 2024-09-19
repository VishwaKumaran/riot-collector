from fastapi import APIRouter

from .champion import router as champion_router
from .item import router as item_router
from .patch import router as patch_router
from .perks import router as perks_router
from .scheduler import router as scheduler_router
from .summoner_spell import router as summoner_spell_router
from .shard import router as shard_router

api_router = APIRouter()
api_router.include_router(champion_router, tags=['champions'])
api_router.include_router(item_router, tags=['items'])
api_router.include_router(patch_router, tags=['patch'])
api_router.include_router(perks_router, tags=['perks'])
api_router.include_router(summoner_spell_router, tags=['summoner_spells'])
api_router.include_router(shard_router, tags=['shards'])
api_router.include_router(scheduler_router, tags=['jobs'])
