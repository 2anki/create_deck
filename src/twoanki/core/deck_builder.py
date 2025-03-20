import genanki
from typing import Optional
from twoanki.core.models import Deck, Card
from twoanki.services.memory_service import MemoryService

class DeckBuilder:
    def __init__(self, memory_service: MemoryService):
        self.memory_service = memory_service
        
    async def create_deck(self, deck: Deck) -> genanki.Deck:
        """Create an Anki deck from our domain model"""
        anki_deck = genanki.Deck(
            deck_id=deck.deck_id or self._generate_deck_id(),
            name=deck.name,
            description=deck.description or ""
        )
        
        for card in deck.cards:
            note = await self._create_note(card)
            anki_deck.add_note(note)
            
        # Store in memory service for later retrieval
        await self.memory_service.store_deck(deck)
        
        return anki_deck

    async def _create_note(self, card: Card) -> genanki.Note:
        """Convert our Card model to an Anki Note"""
        model = self._get_note_model(card)
        
        return genanki.Note(
            model=model,
            fields=[card.front, card.back],
            tags=card.tags
        )
    
    def _generate_deck_id(self) -> int:
        """Generate a random deck ID"""
        import random
        return random.randrange(1 << 30, 1 << 31)
    
    def _get_note_model(self, card: Card) -> genanki.Model:
        """Get the appropriate note model based on card type"""
        model_id = 1483883320
        if card.cloze:
            return genanki.CLOZE_MODEL
        elif card.enable_input:
            model_id = 1483883321
            
        return genanki.Model(
            model_id,
            'Basic',
            fields=[
                {'name': 'Front'},
                {'name': 'Back'},
            ],
            templates=[{
                'name': 'Card 1',
                'qfmt': '{{Front}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{Back}}',
            }],
        ) 