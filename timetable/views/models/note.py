from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class NoteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    content: str
    created: datetime


class NoteForm(BaseModel):
    content: str = Field(min_length=1)
