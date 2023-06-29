from datetime import datetime

import click
from dateutil.relativedelta import relativedelta
from sqlalchemy import func, select

from timetable import app, db
from timetable.models.note import Note
from timetable.services import note as note_svc


@app.cli.command()
@click.argument('keep_days', default=30)
@click.argument('keep_records', default=30)
def archive_notes(keep_days: int, keep_records: int):
    user_ids = db.session.scalars(select(Note.user_id.distinct())).all()
    for user_id in user_ids:
        app.logger.info('Process user_id=%d', user_id)
        process_user(user_id, keep_days, keep_records)


def process_user(user_id: int, keep_days: int, keep_records: int):
    max_created_records = db.session.scalar(
        select(Note.created)
        .filter_by(user_id=user_id)
        .order_by(Note.created.desc())
        .offset(keep_records),
    )

    if max_created_records is None:
        app.logger.info('No record to archive.')
        return

    max_date = datetime.now() - relativedelta(days=keep_days)
    max_created_days = db.session.scalar(
        select(func.max(Note.created))
        .filter_by(user_id=user_id)
        .where(Note.created < max_date.strftime('%Y-%m-%d')),
    )

    if max_created_days is None:
        app.logger.info('No record to archive.')
        return

    max_created = min(max_created_records, max_created_days)
    note_ids = db.session.scalars(
        select(Note.id)
        .filter_by(user_id=user_id)
        .where(Note.created <= max_created),
    ).all()

    note_svc.delete_by_ids(note_ids)
    db.session.commit()

    app.logger.info('Deleted %d rows.', len(note_ids))
