from pydantic import BaseModel
from typing import List
from typing import Dict, List, Optional

class ChatMessage(BaseModel):
    sender: str
    text: str

class ChatData(BaseModel):
    title: str
    messages: List[ChatMessage]
    starred: Optional[bool] = False
    lastColor: Optional[str] = None

class SearchPayload(BaseModel):
    chats: Dict[str, ChatData]
    query: str
    
class JournalEntry(BaseModel):
    text: str

class MoodEntry(BaseModel):
    emotion: str
    confidence: float
    timestamp: int

class MoodLogPayload(BaseModel):
    entries: List[MoodEntry]