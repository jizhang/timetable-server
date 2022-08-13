from flask import make_response, Response
from timetable import app, AppError

InvalidUsage = AppError


@app.errorhandler(AppError)
def handle_app_error(error: AppError) -> Response:
    return make_response(str(error), error.status_code)


@app.get("/api/ping")
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
    resp = make_response("pong")
    resp.mimetype = "text/plain"
    return resp


# pylint: disable=cyclic-import,wrong-import-position
import timetable.views.event
import timetable.views.note
