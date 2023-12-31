from datetime import datetime
from typing import Optional

from flask_login import current_user
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from timetable.consts import CATEGORIES
from timetable.services import event as event_svc

from . import PositiveInt


class Category(BaseModel):
    id: int
    title: str
    color: str


class CategoryResponse(BaseModel):
    categories: list[Category]


class EventId(BaseModel):
    id: PositiveInt

    @field_validator('id')
    @classmethod
    def validate_id(cls, value: int) -> int:
        if event_svc.get_event(current_user.id, value) is None:
            raise ValueError('Event not found')
        return value


class EventListRequest(BaseModel):
    start: datetime
    end: datetime


class Event(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category_id: int = Field(serialization_alias='categoryId')
    title: str
    start: datetime
    end: datetime


class EventListResponse(BaseModel):
    events: list[Event]


class EventForm(BaseModel):
    id: Optional[PositiveInt] = None
    category_id: PositiveInt = Field(alias='categoryId')
    title: str
    start: datetime
    end: datetime

    @field_validator('id')
    @classmethod
    def validate_id(cls, value: int) -> int:  # TODO Optional
        if event_svc.get_event(current_user.id, value) is None:
            raise ValueError('Event not found')
        return value

    @field_validator('category_id')
    @classmethod
    def validate_category_id(cls, value: int) -> int:
        for category in CATEGORIES:
            if value == category['id']:
                return value
        raise ValueError('Invalid category ID')

    @model_validator(mode='after')
    def validate_time_range(self) -> 'EventForm':
        if self.start > self.end:
            raise ValueError('Invalid start/end time')
        return self
