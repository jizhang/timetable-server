# -*- coding: utf-8 -*-

import os
import re
import time
from flask import request, jsonify, render_template
from timetable import app, db
from timetable.views import InvalidUsage
from timetable.models.note import Note


@app.route('/event/index')
def event_index():
    categories = [
        {'id': 1, 'title': 'Work', 'color': '#3a87ad'},
		{'id': 2, 'title': 'Meeting', 'color': 'gray'},
		{'id': 3, 'title': 'Self-achievement', 'color': '#ff9c29'},
		{'id': 4, 'title': 'Goofing-around', 'color': 'black'}
    ]

    note = db.session.query(Note).\
        order_by(Note.id.desc()).\
        first()
    if note is None:
        note_content = ''
    else:
        note_content = note.content

    return render_template('event/index.html',
                           categories=categories,
                           note_content=note_content)


@app.route('/event/save', methods=['POST'])
def event_save():
    return jsonify('ok')
