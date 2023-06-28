from datetime import datetime
from typing import List, Optional

from sqlalchemy import delete, select

from timetable import db, utils
from timetable.models.note import Note


def get_note_content(user_id: int) -> str:
    note_content: Optional[str] = db.session.scalar(
        select(Note.content)
        .filter_by(user_id=user_id)
        .order_by(Note.id.desc()),
    )
    return note_content or ''


def save(note: Note):
    note.created = datetime.now()
    db.session.add(note)


def delete_by_ids(ids: List[int]):
    for chunk in utils.chunks(ids, 100):
        db.session.execute(
            delete(Note)
            .where(Note.id.in_(chunk)),
        )
