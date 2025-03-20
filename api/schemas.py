from pydantic import BaseModel
from typing import List
from ..core.models import Card, DeckSettings, Deck

class CreateDeckRequest(BaseModel):
    deck: Deck

class CreateDeckResponse(BaseModel):
    deck_id: int
    download_url: str 