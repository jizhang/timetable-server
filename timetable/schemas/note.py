from marshmallow import Schema, fields


class NoteFormSchema(Schema):
    content = fields.Str()


class NoteSchema(Schema):
    content = fields.Str()
    created = fields.DateTime()


note_form_schema = NoteFormSchema()
note_schema = NoteSchema()
