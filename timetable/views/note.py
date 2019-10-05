import datetime

from flask import request, jsonify

from timetable import app, db, auth
from timetable.models.note import Note

@app.route('/note/save', methods=['POST'])
@auth.login_required
def note_save():
    note = Note()
    note.content = request.form.get('content', '')
    note.created = datetime.datetime.now()
    db.session.add(note)
    db.session.commit()
    return jsonify('Saved {}'.format(note.created.strftime('%Y-%m-%d %H:%M:%S')))
