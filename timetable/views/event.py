# -*- coding: utf-8 -*-

import os
import re
import time
import datetime
from flask import request, jsonify, render_template
from timetable import app, db
from timetable.views import InvalidUsage
from timetable.models.note import Note
from timetable.models.event import Event


CATEGORIES = [
    {'id': 1, 'title': 'Work', 'color': '#3a87ad'},
    {'id': 2, 'title': 'Meeting', 'color': 'gray'},
    {'id': 3, 'title': 'Self-achievement', 'color': '#ff9c29'},
    {'id': 4, 'title': 'Goofing-around', 'color': 'black'}
]


@app.route('/event/index')
def event_index():
    note = db.session.query(Note).\
        order_by(Note.id.desc()).\
        first()
    if note is None:
        note_content = ''
    else:
        note_content = note.content

    return render_template('event/index.html',
                           categories=CATEGORIES,
                           note_content=note_content)


@app.route('/event/ping', methods=['POST'])
def event_ping():
    return jsonify('pong')


@app.route('/event/list')
def event_list():
    try:
        start = datetime.datetime.strptime(request.args['start'], '%Y-%m-%d')
        end = datetime.datetime.strptime(request.args['end'], '%Y-%m-%d')
    except Exception:
        raise InvalidUsage('invalid dates')

    rows = db.session.query(Event).\
        filter(Event.start >= start.strftime('%Y-%m-%d 00:00:00')).\
        filter(Event.start <= end.strftime('%Y-%m-%d 23:59:59')).\
        order_by(Event.id).\
        all()

    events = []
    for row in rows:
        events.append({
            'id': row.id,
            'title': row.title,
            'start': row.start.strftime('%Y-%m-%d %H:%M:%S'),
            'end': row.end.strftime('%Y-%m-%d %H:%M:%S'),
            'categoryId': row.category_id,
            'color': get_category_color(row.category_id)
        })


    return jsonify(events)


def get_category_color(category_id):
    for item in CATEGORIES:
        if item['id'] == category_id:
            return item['color']
    return ''


@app.route('/event/save', methods=['POST'])
def event_save():
    event = None
    event_id = request.form.get('id')
    if event_id:
        event = db.session.query(Event).get(event_id)
    if event is None:
        event = Event()
        event.created = datetime.datetime.now()
        db.session.add(event)

    title = request.form.get('title', '').strip()
    if not title:
        raise InvalidUsage('title cannot be empty')

    try:
        category_id = int(request.form['categoryId'])
    except Exception:
        raise InvalidUsage('invalid categoryId')

    try:
        start = datetime.datetime.strptime(request.form['start'], '%Y-%m-%d %H:%M:%S')
        end = datetime.datetime.strptime(request.form['end'], '%Y-%m-%d %H:%M:%S')
        if end < start:
            raise ValueError()
    except Exception:
        raise InvalidUsage('invalid start / end')

    event.title = title
    event.category_id = category_id
    event.start = start
    event.end = end
    event.updated = datetime.datetime.now()
    db.session.add(event)
    db.session.commit()

    return jsonify({'id': event.id})


@app.route('/event/delete', methods=['POST'])
def event_delete():
    if not request.form.get('id'):
        raise InvalidUsage('id cannot be empty')
    row = db.session.query(Event).get(request.form['id'])
    if row is None:
        raise InvalidUsage('event not found')
    db.session.delete(row)
    db.session.commit()
    return jsonify('ok')
