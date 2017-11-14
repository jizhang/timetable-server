# -*- coding: utf-8 -*-

import os
from functools import wraps
from flask import make_response, session, abort, redirect, url_for, request
from timetable import app


class InvalidUsage(Exception):
    status_code = 400


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    return make_response(str(error), error.status_code)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('timetable_user'):
            return redirect(url_for('login', next=request.url))
        elif session['timetable_user'] not in app.config['TIMETABLE_ADMIN']:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


# load views
from timetable.views import index
from timetable.views import event
from timetable.views import note
