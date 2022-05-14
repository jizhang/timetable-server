import datetime

from flask import request, jsonify, Response

from timetable import app, db, auth
from timetable.models.note import Note


@app.post('/note/save')
@auth.login_required
def note_save() -> Response:
    note = Note()
    note.content = request.form.get('content', '')
    note.created = datetime.datetime.now()
    db.session.add(note)
    db.session.commit()

    created = note.created.strftime('%Y-%m-%d %H:%M:%S')
    return jsonify(f'Saved {created}')
