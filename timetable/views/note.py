from datetime import datetime

from flask import request
from marshmallow import ValidationError

from timetable import app, db, auth, AppError
from timetable.models.note import Note
from timetable.schemas.note import note_form_schema, note_schema


@app.post('/note/save')
@auth.login_required
def note_save() -> dict:
    """
    ---
    post:
      summary: Save note.
      requestBody:
        required: true
        content:
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/NoteForm'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Note'
    """
    try:
        note_form = note_form_schema.load(request.form)
    except ValidationError as e:
        raise AppError(e.messages)

    note = Note(**note_form)
    note.created = datetime.now()
    db.session.add(note)
    db.session.commit()

    return note_schema.dump(note)
