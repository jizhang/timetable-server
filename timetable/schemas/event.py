from typing import Any, Optional, Dict

from flask_login import current_user
from marshmallow import (
    Schema,
    fields,
    validate,
    validates,
    validates_schema,
    ValidationError,
    post_load,
)

from timetable import db
from timetable.consts import CATEGORIES
from timetable.models.event import Event
from timetable.services import event as event_svc


class CategorySchema(Schema):
    id = fields.Integer()
    title = fields.String()
    color = fields.String()


class EventSchema(Schema):
    id = fields.Integer()
    category_id = fields.Integer(data_key="categoryId", required=True)
    title = fields.String(required=True, validate=validate.Length(min=1))
    start = fields.DateTime(required=True)
    end = fields.DateTime(required=True)

    @validates("id")
    def validate_id(self, value: Optional[int]):
        if not value:
            return
        event = db.session.query(Event).get(value)
        if event is None:
            raise ValidationError("Event not found.")

    @validates("category_id")
    def validate_category_id(self, value: int):
        for category in CATEGORIES:
            if value == category["id"]:
                return
        raise ValidationError("Invalid category ID.")

    @validates_schema
    def validate_schema(self, data: Dict[str, Any], **kwargs):
        if data["end"] < data["start"]:
            raise ValidationError("Invalid start/end time.")


class EventIdSchema(Schema):
    id = fields.Int(required=True)

    @post_load
    def make_event(self, data, **kwargs):
        row = event_svc.get_event(current_user.id, data["id"])
        if row is None:
            raise ValidationError("Event not found")
        return row


category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
event_schema = EventSchema()
event_id_schema = EventIdSchema()
