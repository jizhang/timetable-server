from marshmallow import Schema, fields


class CurrentUserSchema(Schema):
    id = fields.Int()
    username = fields.Str()


current_user_schema = CurrentUserSchema()
