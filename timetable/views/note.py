# -*- coding: utf-8 -*-

from flask import jsonify
from timetable import app


@app.route('/note/save')
def note_save():
    return jsonify('ok')
