from datetime import datetime
from typing import Sequence

from sqlalchemy import delete, select

from timetable import db, utils
from timetable.models.note import Note


def get_or_create_note(user_id: int) -> Note:
    note = db.session.scalar(
        select(Note)
        .filter_by(user_id=user_id)
        .order_by(Note.id.desc()),
    )
    if note is None:
        note = Note(user_id=user_id, content='', created=datetime.now())
    return note


def save(note: Note):
    note.created = datetime.now()
    db.session.add(note)


def delete_by_ids(ids: Sequence[int]):
    for chunk in utils.chunks(ids, 100):
        db.session.execute(
            delete(Note)
            .where(Note.id.in_(chunk)),
        )
