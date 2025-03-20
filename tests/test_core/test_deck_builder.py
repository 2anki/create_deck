import pytest
from unittest.mock import AsyncMock
from twoanki.core.deck_builder import DeckBuilder
from twoanki.core.models import Deck, Card, DeckSettings

@pytest.mark.asyncio
async def test_create_deck(mock_memory_service):
    deck_builder = DeckBuilder(mock_memory_service)
    
    test_deck = Deck(
        name="Test Deck",
        cards=[
            Card(
                front="Question 1",
                back="Answer 1",
                tags=["test"]
            )
        ],
        settings=DeckSettings()
    )
    
    result = await deck_builder.create_deck(test_deck)
    
    assert result.name == test_deck.name
    mock_memory_service.store_deck.assert_called_once_with(test_deck)

@pytest.mark.asyncio
async def test_create_note():
    deck_builder = DeckBuilder(AsyncMock())
    
    test_card = Card(
        front="Test Question",
        back="Test Answer",
        tags=["test"],
        cloze=False,
        enable_input=False
    )
    
    note = await deck_builder._create_note(test_card)
    assert note.fields[0] == "Test Question"
    assert note.fields[1] == "Test Answer" 