from fastapi import APIRouter

from app.crud.summoner_spell import SummonerSpell
from app.schema.summoner_spell import SummonerSpellSchema

router = APIRouter()


@router.post('/summoner-spells')
async def create_summoner_spell(summoner_spell: SummonerSpellSchema):
    result = await SummonerSpell.add(summoner_spell)
    return result
