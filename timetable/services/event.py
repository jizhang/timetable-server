from datetime import datetime
from typing import Optional, Sequence

from dateutil.tz import tzlocal
from sqlalchemy import select

from timetable import db
from timetable.models.event import Event


def get_event(user_id: int, event_id: int) -> Optional[Event]:
    return db.session.scalar(
        select(Event)
        .filter_by(user_id=user_id, id=event_id),
    )


def save(event: Event) -> int:
    if not event.id:
        event.created = datetime.now()

    event.start = event.start.astimezone(tzlocal())
    event.end = event.end.astimezone(tzlocal())
    saved_event = db.session.merge(event)
    db.session.flush()

    return saved_event.id


def get_event_list(user_id: int, start: datetime, end: datetime) -> Sequence[Event]:
    return db.session.scalars(
        select(Event)
        .filter_by(user_id=user_id)
        .where(Event.start >= start.astimezone(tzlocal()))
        .where(Event.start < end.astimezone(tzlocal())),
    ).all()


def delete_event(event_id: int):
    event = db.session.get(Event, event_id)
    assert event is not None
    db.session.delete(event)
