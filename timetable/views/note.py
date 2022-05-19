from datetime import datetime

from flask import request
from marshmallow import ValidationError

from timetable import app, db, auth, AppError
from timetable.models.note import Note
from timetable.services import note as note_service
from timetable.schemas.note import note_form_schema, note_schema


@app.get('/note/content')
@auth.login_required
def get_note_content() -> dict:
    """
    ---
    get:
      summary: Get note content.
      tags: [note]
      x-swagger-router-controller: timetable.views.note
      operationId: get_note_content
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/NoteForm'
    """
    content = note_service.get_note_content()
    return note_form_schema.dump({'content': content})


@app.post('/note/save')
@auth.login_required
def save_note() -> dict:
    """
    ---
    post:
      summary: Save note.
      tags: [note]
      x-swagger-router-controller: timetable.views.note
      operationId: save_note
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
