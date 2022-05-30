from datetime import datetime

from timetable import db
from timetable.models.event import Event


def save(event: Event) -> int:
    if not event.id:
        event.id = None
        event.created = datetime.now()

    event.updated = datetime.now()
    saved_event = db.session.merge(event)
    db.session.flush()

    return saved_event.id
