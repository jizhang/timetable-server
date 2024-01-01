from flask import Response, request
from flask_login import current_user, login_required

from timetable import app, db
from timetable.models.note import Note
from timetable.services import note as note_svc

from . import send_json
from .models.note import Note as NoteResponse
from .models.note import NoteForm


def send_note(note: Note) -> Response:
    note_response = NoteResponse.model_validate(note, from_attributes=True)
    return send_json(note_response.model_dump_json())


@app.get('/api/note/content')
@login_required
def get_note_content() -> Response:
    return send_note(note_svc.get_or_create_note(current_user.id))


@app.post('/api/note/save')
@login_required
def save_note() -> Response:
    form = NoteForm.model_validate(request.json)
    note = Note(**dict(form), user_id=current_user.id)
    note_svc.save(note)
    db.session.commit()
    return send_note(note)
