from marshmallow import Schema, fields


class NoteForm(Schema):
    content = fields.Str()
