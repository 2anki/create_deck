import pytest
from unittest.mock import patch, AsyncMock
from twoanki.services.memory_service import MemoryService
from twoanki.core.models import Deck, Card, DeckSettings

@pytest.mark.asyncio
async def test_store_deck():
    with patch('redis.Redis') as mock_redis:
        memory_service = MemoryService()
        mock_redis_instance = AsyncMock()
        mock_redis.return_value = mock_redis_instance
        
        test_deck = Deck(
            deck_id=1,
            name="Test Deck",
            cards=[],
            settings=DeckSettings()
        )
        
        await memory_service.store_deck(test_deck)
        mock_redis_instance.set.assert_called_once()

@pytest.mark.asyncio
async def test_get_deck():
    with patch('redis.Redis') as mock_redis:
        memory_service = MemoryService()
        mock_redis_instance = AsyncMock()
        mock_redis.return_value = mock_redis_instance
        
        test_deck = Deck(
            deck_id=1,
            name="Test Deck",
            cards=[],
            settings=DeckSettings()
        )
        mock_redis_instance.get.return_value = test_deck.json()
        
        result = await memory_service.get_deck(1)
        assert isinstance(result, Deck)
        assert result.deck_id == 1
        assert result.name == "Test Deck"

@pytest.mark.asyncio
async def test_get_nonexistent_deck():
    with patch('redis.Redis') as mock_redis:
        memory_service = MemoryService()
        mock_redis_instance = AsyncMock()
        mock_redis.return_value = mock_redis_instance
        
        mock_redis_instance.get.return_value = None
        
        result = await memory_service.get_deck(999)
        assert result is None 