from fastapi import APIRouter, HTTPException
from .schemas import CreateDeckRequest, CreateDeckResponse
from ..core.deck_builder import DeckBuilder
from ..services.memory_service import MemoryService

router = APIRouter()
memory_service = MemoryService()
deck_builder = DeckBuilder(memory_service)

@router.post("/decks", response_model=CreateDeckResponse)
async def create_deck(request: CreateDeckRequest):
    try:
        deck = await deck_builder.create_deck(request.deck)
        return CreateDeckResponse(
            deck_id=deck.deck_id,
            download_url=f"/decks/{deck.deck_id}/download"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 