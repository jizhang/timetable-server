from flask import request, Response
from flask_login import login_required, current_user
from marshmallow import ValidationError

from timetable import app, db, AppError
from timetable.models.note import Note
from timetable.services import note as note_service
from timetable.schemas.note import note_form_schema, note_schema


@app.get("/api/note/content")
@login_required
def get_note_content() -> Response:
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
    content = note_service.get_note_content(current_user.id)
    return note_form_schema.dump({"content": content})


@app.post("/api/note/save")
@login_required
def save_note() -> Response:
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
          application/json:
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
        note_form = note_form_schema.load(request.json)  # type: ignore
    except ValidationError as e:
        raise AppError(str(e.messages))

    note = Note(**note_form, user_id=current_user.id)
    note_service.save(note)
    db.session.commit()

    return note_schema.dump(note)
