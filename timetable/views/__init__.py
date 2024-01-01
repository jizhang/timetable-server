from flask import Response, jsonify
from pydantic import ValidationError

from timetable import AppError, app


@app.errorhandler(AppError)
def handle_app_error(error: AppError) -> tuple[Response, int]:
    payload = {
        'code': error.code,
        'message': error.message,
    }
    return jsonify(payload), 400


@app.errorhandler(ValidationError)
def handle_validation_error(error: ValidationError) -> tuple[Response, int]:
    detail = error.errors()[0]
    payload = {
        'code': 400,
        'message': f'{detail["loc"][0]}: {detail["msg"]}',
    }
    return jsonify(payload), 400


@app.get('/api/ping')
def ping() -> Response:
    return Response('pong', mimetype='text/plain')


import timetable.views.event
import timetable.views.note
import timetable.views.user
