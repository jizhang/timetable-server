from datetime import datetime

from pydantic import BaseModel, Field


class Note(BaseModel):
    content: str
    created: datetime


class NoteForm(BaseModel):
    content: str = Field(min_length=1)
