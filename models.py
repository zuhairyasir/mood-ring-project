from pydantic import BaseModel
from typing import List

class JournalEntry(BaseModel):
    text: str

class MoodEntry(BaseModel):
    emotion: str
    confidence: float
    timestamp: int

class MoodLogPayload(BaseModel):
    entries: List[MoodEntry]