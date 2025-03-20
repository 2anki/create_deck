from typing import List, Optional
from pydantic import BaseModel

class CardSchema(BaseModel):
    front: str
    back: str
    tags: List[str] = []
    cloze: bool = False
    enable_input: bool = False
    media: List[str] = []

class DeckSettingsSchema(BaseModel):
    use_input: bool = False
    max_one: bool = True
    no_underline: bool = False
    template: str = "specialstyle"

class DeckSchema(BaseModel):
    name: str
    cards: List[CardSchema]
    settings: DeckSettingsSchema
    description: Optional[str] = None
    deck_id: Optional[int] = None

class CreateDeckRequest(BaseModel):
    deck: DeckSchema

class CreateDeckResponse(BaseModel):
    deck_id: int
    download_url: str 