from datetime import datetime

from pydantic import BaseModel


class Note(BaseModel):
    content: str
    created: datetime


class NoteForm(BaseModel):
    content: str = ''
