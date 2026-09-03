from pydantic import BaseModel, Field
from typing import Dict, List, Optional

class JournalEntry(BaseModel):
    text: str = Field(min_length=1, max_length=1000)

class MoodEntry(BaseModel):
    emotion: str
    confidence: float
    timestamp: int

class MoodLogPayload(BaseModel):
    entries: List[MoodEntry]

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

class ExplainPayload(BaseModel):
    text: str
    emotion: str

class SignupPayload(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    email: str = Field(min_length=5, max_length=100)
    password: str = Field(min_length=6, max_length=100)

class LoginPayload(BaseModel):
    email: str
    password: str