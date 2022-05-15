from flask import make_response
from timetable import app, AppError

InvalidUsage = AppError


@app.errorhandler(AppError)
def handle_app_error(error: AppError):
    return make_response(str(error), error.status_code)


# pylint: disable=cyclic-import,wrong-import-position
from timetable.views import index
from timetable.views import event
from timetable.views import note
