from flask import request
from flask_login import current_user, login_required

from timetable import app, db
from timetable.models.note import Note
from timetable.services import note as note_svc

from .models.note import Note as NoteResponse
from .models.note import NoteForm


@app.get('/api/note/content')
@login_required
def get_note_content() -> dict:
    content = note_svc.get_note_content(current_user.id)
    return NoteForm(content=content).model_dump()  ## TODO Return NoteResponse


@app.post('/api/note/save')
@login_required
def save_note() -> dict:
    form = NoteForm.model_validate(request.json)
    note = Note(**dict(form), user_id=current_user.id)
    note_svc.save(note)
    db.session.commit()

    resp = NoteResponse.model_validate(note, from_attributes=True)
    return resp.model_dump()
