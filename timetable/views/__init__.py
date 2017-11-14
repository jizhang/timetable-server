# -*- coding: utf-8 -*-

import os
from flask import make_response, redirect, url_for
from timetable import app


class InvalidUsage(Exception):
    status_code = 400


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    return make_response(str(error), error.status_code)


@app.route('/')
def index():
    return redirect(url_for('event_index'))


# load views
from timetable.views import event
from timetable.views import note
