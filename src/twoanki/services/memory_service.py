from typing import Optional
import redis
from twoanki.core.models import Deck

class MemoryService:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        
    async def store_deck(self, deck: Deck) -> None:
        """Store a deck in Redis"""
        key = f"deck:{deck.deck_id}"
        self.redis_client.set(key, deck.json())
        
    async def get_deck(self, deck_id: int) -> Optional[Deck]:
        """Retrieve a deck from Redis"""
        key = f"deck:{deck_id}"
        data = self.redis_client.get(key)
        if data:
            return Deck.parse_raw(data)
        return None 