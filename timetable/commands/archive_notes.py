from datetime import datetime

import click
from sqlalchemy import func
from dateutil.relativedelta import relativedelta

from timetable import app, db
from timetable.models.note import Note
from timetable.services import note as note_svc


@app.cli.command()
@click.argument('keep_days', default=30)
@click.argument('keep_records', default=30)
def archive_notes(keep_days: int, keep_records: int):
    rows = db.session.query(Note.user_id.distinct()).all()
    for row in rows:
        user_id: int = row[0]
        app.logger.info('Process user_id=%d', user_id)
        process_user(user_id, keep_days, keep_records)


def process_user(user_id: int, keep_days: int, keep_records: int):
    max_created_records = (
        db.session.query(Note.created)
        .filter_by(user_id=user_id)
        .order_by(Note.created.desc())
        .offset(keep_records)
        .limit(1)
        .scalar()
    )

    if max_created_records is None:
        app.logger.info('No record to archive.')
        return

    max_date = datetime.now() - relativedelta(days=keep_days)
    max_created_days = (
        db.session.query(func.max(Note.created))
        .filter_by(user_id=user_id)
        .filter(Note.created < max_date.strftime('%Y-%m-%d'))
        .scalar()
    )

    if max_created_days is None:
        app.logger.info('No record to archive.')
        return

    max_created = min(max_created_records, max_created_days)
    rows = (
        db.session.query(Note.id)
        .filter_by(user_id=user_id)
        .filter(Note.created <= max_created)
        .all()
    )

    note_svc.delete_by_ids([row.id for row in rows])
    db.session.commit()

    app.logger.info('Deleted %d rows.', len(rows))
