from pydantic import BaseModel

class JournalEntry(BaseModel):
    text: str