from datetime import datetime

from timetable import db
from timetable.models.event import Event


def save(event: Event):
    if not event.id:
        event.created = datetime.now()
    db.session.merge(event)
    event.updated = datetime.now()
