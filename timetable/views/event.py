# -*- coding: utf-8 -*-

import os
import re
import time
from flask import request, jsonify
from timetable import app
from timetable.views import InvalidUsage


@app.route('/event/index')
def event_index():
    return render_template('event/index.html')


@app.route('/event/save', methods=['POST'])
def event_save():
    return jsonify('ok')
