from flask import request
from flask_login import current_user, login_required

from timetable import app, db
from timetable.models.note import Note
from timetable.services import note as note_svc

from .models.note import NoteForm, NoteResponse


@app.get('/api/note/content')
@login_required
def get_note_content() -> dict:
    note = note_svc.get_or_create_note(current_user.id)
    resp = NoteResponse.model_validate(note)
    return resp.model_dump(mode='json')


@app.post('/api/note/save')
@login_required
def save_note() -> dict:
    form = NoteForm.model_validate(request.json)
    note = Note(**dict(form), user_id=current_user.id)
    note_svc.save(note)
    db.session.commit()

    resp = NoteResponse.model_validate(note)
    return resp.model_dump(mode='json')
