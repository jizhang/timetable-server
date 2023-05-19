from typing import Optional, List
from datetime import datetime
from dateutil.tz import tzlocal

from timetable import db
from timetable.models.event import Event


def get_event(user_id: int, event_id: int) -> Optional[Event]:
    return db.session.query(Event).filter_by(user_id=user_id, id=event_id).first()


def save(event: Event) -> int:
    if not event.id:
        event.id = None
        event.created = datetime.now()

    event.start = event.start.astimezone(tzlocal())
    event.end = event.end.astimezone(tzlocal())
    saved_event = db.session.merge(event)
    db.session.flush()

    return saved_event.id


def get_event_list(user_id: int, start: datetime, end: datetime) -> List[Event]:
    return (
        db.session.query(Event)
        .filter_by(user_id=user_id)
        .filter(Event.start >= start.astimezone(tzlocal()))
        .filter(Event.start < end.astimezone(tzlocal()))
        .all()
    )
