from typing import Any, Optional, Dict

from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError

from timetable import db
from timetable.consts import CATEGORIES
from timetable.models.event import Event

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class CategorySchema(Schema):
    id = fields.Integer()
    title = fields.String()
    color = fields.String()


class EventSchema(Schema):
    id = fields.Integer()
    category_id = fields.Integer(data_key='categoryId', required=True)
    title = fields.String(required=True, validate=validate.Length(min=1))
    start = fields.DateTime(required=True, format=DATETIME_FORMAT)
    end = fields.DateTime(required=True, format=DATETIME_FORMAT)

    @validates('id')
    def validate_id(self, value: Optional[int]):
        if not value:
            return
        event = db.session.query(Event).get(value)
        if event is None:
            raise ValidationError('Event not found.')

    @validates('category_id')
    def validate_category_id(self, value: int):
        for category in CATEGORIES:
            if value == category['id']:
                return
        raise ValidationError('Invalid category ID.')

    @validates_schema
    def validate_schema(self, data: Dict[str, Any], **kwargs):
        if data['end'] < data['start']:
            raise ValidationError('Invalid start/end time.')


category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
event_schema = EventSchema()
events_schema = EventSchema(many=True)
