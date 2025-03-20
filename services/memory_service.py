from typing import Optional, Dict
from ..core.models import Deck
import redis
from pydantic import parse_raw_as

class MemoryService:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        
    async def store_deck(self, deck: Deck) -> None:
        key = f"deck:{deck.deck_id}"
        await self.redis_client.set(key, deck.json())
        
    async def get_deck(self, deck_id: int) -> Optional[Deck]:
        key = f"deck:{deck_id}"
        data = await self.redis_client.get(key)
        if data:
            return parse_raw_as(Deck, data)
        return None 