from fastapi import APIRouter, HTTPException
from twoanki.api.schemas import CreateDeckRequest, CreateDeckResponse
from twoanki.core.deck_builder import DeckBuilder
from twoanki.services.memory_service import MemoryService

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

@router.get("/decks/{deck_id}")
async def get_deck(deck_id: int):
    deck = await memory_service.get_deck(deck_id)
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")
    return deck 