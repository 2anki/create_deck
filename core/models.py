from pydantic import BaseModel
from typing import List, Optional

class Card(BaseModel):
    front: str
    back: str
    tags: List[str] = []
    cloze: bool = False
    enable_input: bool = False
    media: List[str] = []

class DeckSettings(BaseModel):
    use_input: bool = False
    max_one: bool = True
    no_underline: bool = False
    template: str = "specialstyle"

class Deck(BaseModel):
    name: str
    cards: List[Card]
    settings: DeckSettings
    description: Optional[str] = None
    deck_id: Optional[int] = None 