from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

from timetable import app
from timetable.schemas.note import NoteFormSchema, NoteSchema
from timetable.views.note import save_note

spec = APISpec(
    title='Timetable',
    version='0.1.0',
    openapi_version='3.0.2',
    info={'description': 'What have you done today?'},
    servers=[{'url': 'http://localhost:1234'}],
    plugins=[FlaskPlugin(), MarshmallowPlugin()]
)

spec.components.schema('NoteForm', schema=NoteFormSchema)
spec.components.schema('Note', schema=NoteSchema)

with app.test_request_context():
    spec.path(view=save_note)
