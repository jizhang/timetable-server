from typing import Any, Optional, Dict
from datetime import datetime

from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError

from timetable import db
from timetable.consts import CATEGORIES
from timetable.models.event import Event


class CategorySchema(Schema):
    id = fields.Integer()
    title = fields.String()
    color = fields.String()


class EventSchema(Schema):
    id = fields.Integer()
    category_id = fields.Integer(data_key='categoryId', required=True)
    title = fields.String(required=True, validate=validate.Length(min=1))
    start = fields.String(required=True)
    end = fields.String(required=True)

    @validates('id')
    def validate_id(self, value: Optional[int]):
        if not value:
            return
        event = db.sesssion.query(Event).get(value)
        if event is None:
            raise ValidationError('Event not found.')

    @validates('category_id')
    def validate_category_id(self, value: int):
        for category in CATEGORIES:
            if value == category['id']:
                return
        raise ValidationError('Invalid category ID.')

    @validates('start')
    def validate_start(self, value: str):
        self.validate_datetime(value, 'start')

    @validates('end')
    def validate_start(self, value: str):
        self.validate_datetime(value, 'end')

    @validates_schema
    def validate_schema(self, data: Dict[str, Any]):
        if data['end'] < data['start']:
            raise ValidationError('Invalid start/end time.')

    def validate_datetime(self, value: str, field: str):
        try:
            datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        except ValueError as e:
            raise ValidationError(f'Invalid {field} time.') from e


category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
event_schema = EventSchema()
events_schema = EventSchema(many=True)
