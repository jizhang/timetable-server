# mypy: ignore-errors
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

from timetable import app
from timetable.schemas import event as event_schemas
from timetable.schemas.current_user import CurrentUserSchema
from timetable.schemas.login_form import LoginFormSchema
from timetable.schemas.note import NoteFormSchema, NoteSchema
from timetable.views import event as event_view
from timetable.views import note as note_view
from timetable.views import ping
from timetable.views import user as user_view

spec = APISpec(
    title='Timetable',
    version='0.1.0',
    openapi_version='3.0.2',
    info={'description': 'What have you done today?'},
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

spec.components.schema('LoginForm', schema=LoginFormSchema)
spec.components.schema('CurrentUser', schema=CurrentUserSchema)
spec.components.schema('Category', schema=event_schemas.CategorySchema)
spec.components.schema('Event', schema=event_schemas.EventSchema)
spec.components.schema('EventId', schema=event_schemas.EventIdSchema)
spec.components.schema('NoteForm', schema=NoteFormSchema)
spec.components.schema('Note', schema=NoteSchema)

with app.test_request_context():
    spec.path(view=ping)
    spec.path(view=user_view.user_login)
    spec.path(view=event_view.get_event_categories)
    spec.path(view=event_view.save_event)
    spec.path(view=event_view.get_event_list)
    spec.path(view=event_view.delete_event)
    spec.path(view=note_view.get_note_content)
    spec.path(view=note_view.save_note)
