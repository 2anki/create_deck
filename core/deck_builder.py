from typing import List
import genanki
from .models import Deck, Card
from ..services.memory_service import MemoryService

class DeckBuilder:
    def __init__(self, memory_service: MemoryService):
        self.memory_service = memory_service
        
    async def create_deck(self, deck: Deck) -> genanki.Deck:
        # Convert our domain model to Anki format
        anki_deck = genanki.Deck(
            deck_id=deck.deck_id or self._generate_deck_id(),
            name=deck.name,
            description=deck.description
        )
        
        for card in deck.cards:
            note = await self._create_note(card)
            anki_deck.add_note(note)
            
        # Store in memory service for later retrieval
        await self.memory_service.store_deck(deck)
        
        return anki_deck

    async def _create_note(self, card: Card) -> genanki.Note:
        # Implementation of note creation logic
        pass 