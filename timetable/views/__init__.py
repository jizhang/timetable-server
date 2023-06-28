from typing import Tuple

from flask import Response, jsonify, make_response

from timetable import AppError, app


@app.errorhandler(AppError)
def handle_app_error(error: AppError) -> Tuple[Response, int]:
    payload = {
        'code': error.code,
        'message': error.message,
    }
    return jsonify(payload), 400


@app.get('/api/ping')
def ping() -> Response:
    """
    ---
    get:
      summary: Ping API server.
      tags: [common]
      x-swagger-router-controller: timetable.views
      operationId: ping
      responses:
        '200':
          description: OK
          content:
            text/plain:
              schema:
                type: string
                example: pong
    """
    resp = make_response('pong')
    resp.mimetype = 'text/plain'
    return resp


import timetable.views.event
import timetable.views.note
import timetable.views.user
