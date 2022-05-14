from flask import make_response
from timetable import app


class InvalidUsage(Exception):
    status_code = 400


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    return make_response(str(error), error.status_code)


# pylint: disable=cyclic-import,wrong-import-position
from timetable.views import index
from timetable.views import event
from timetable.views import note
