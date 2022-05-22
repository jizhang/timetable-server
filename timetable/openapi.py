from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

from timetable import app
from timetable.views import note
from timetable.schemas.note import NoteFormSchema, NoteSchema

spec = APISpec(
    title='Timetable',
    version='0.1.0',
    openapi_version='3.0.2',
    info={'description': 'What have you done today?'},
    servers=[{'url': 'http://localhost:3000'}],
    plugins=[FlaskPlugin(), MarshmallowPlugin()]
)

spec.components.schema('NoteForm', schema=NoteFormSchema)
spec.components.schema('Note', schema=NoteSchema)

with app.test_request_context():
    spec.path(view=note.get_note_content)
    spec.path(view=note.save_note)
