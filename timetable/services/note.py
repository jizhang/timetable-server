from timetable import db
from timetable.models.note import Note


def get_note_content() -> str:
    note = db.session.query(Note).\
        order_by(Note.id.desc()).\
        first()
    return note.content if note is not None else ''
