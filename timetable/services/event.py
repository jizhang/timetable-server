from typing import List
from datetime import datetime
from dateutil.tz import tzlocal

from timetable import db
from timetable.models.event import Event


def save(event: Event) -> int:
    if not event.id:
        event.id = None
        event.created = datetime.now()

    event.start = event.start.astimezone(tzlocal())
    event.end = event.end.astimezone(tzlocal())
    saved_event = db.session.merge(event)
    db.session.flush()

    return saved_event.id


def get_event_list(start: datetime, end: datetime) -> List[Event]:
    return (
        db.session.query(Event)
        .filter(Event.start >= start.astimezone(tzlocal()))
        .filter(Event.start < end.astimezone(tzlocal()))
        .all()
    )
