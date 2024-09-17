from fastapi import HTTPException

from app.core.config import settings
from app.crud import response_creation
from app.db import firebase
from app.schema.summoner_spell import SummonerSpellSchema


class SummonerSpell:
    @staticmethod
    async def add(summoner_spell: SummonerSpellSchema | dict):
        if isinstance(summoner_spell, dict):
            summoner_spell = SummonerSpellSchema(**summoner_spell)

        _summoner_spell: dict = summoner_spell.dict()

        check_summoner_spell = (
            firebase.db.collection(settings.SUMMONER_SPELL_COLLECTION)
            .where('patch', '==', summoner_spell.patch)
            .where('name', '==', summoner_spell.name)
            .limit(1)
            .stream()
        )
        async for _ in check_summoner_spell:
            raise HTTPException(
                400,
                f"Summoner spell {summoner_spell.name} with patch version {summoner_spell.patch} already exists."
            )

        doc_ref = firebase.db.collection(settings.SUMMONER_SPELL_COLLECTION).document()
        await doc_ref.set(_summoner_spell)

        return response_creation(
            f"Summoner spell {summoner_spell.name} with patch version {summoner_spell.patch} successfully added.",
            doc_ref.id
        )
