import dateutil.parser
from flask import Response, jsonify, request
from flask_login import current_user, login_required
from marshmallow import ValidationError

from timetable import AppError, app, db
from timetable.consts import CATEGORIES
from timetable.models.event import Event
from timetable.schemas.event import categories_schema, event_id_schema, event_schema
from timetable.services import event as event_service


@app.get('/api/event/categories')
@login_required
def get_event_categories() -> Response:
    """
    ---
    get:
      summary: Get event categories.
      tags: [event]
      x-swagger-router-controller: timetable.views.event
      operationId: get_event_categories
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                type: object
                properties:
                  categories:
                    type: array
                    items:
                      $ref: '#/components/schemas/Category'
    """
    return jsonify(categories=categories_schema.dump(CATEGORIES))


@app.get('/api/event/list')
@login_required
def get_event_list() -> Response:
    """
    ---
    get:
      summary: Get event list.
      tags: [event]
      x-swagger-router-controller: timetable.views.event
      operationId: get_event_list
      parameters:
        - in: query
          name: start
          schema:
            type: string
            format: date-time
        - in: query
          name: end
          schema:
            type: string
            format: date-time
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                type: object
                properties:
                  events:
                    type: array
                    items:
                      $ref: '#/components/schemas/Event'
    """
    try:
        start = dateutil.parser.parse(request.args['start'])
        end = dateutil.parser.parse(request.args['end'])
    except Exception as e:
        raise AppError('Invalid start or end time.') from e

    events = event_service.get_event_list(current_user.id, start, end)
    return jsonify(events=event_schema.dump(events, many=True))


@app.post('/api/event/save')
@login_required
def save_event() -> Response:
    """
    ---
    post:
      summary: Save event.
      tags: [event]
      x-swagger-router-controller: timetable.views.event
      operationId: save_event
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Event'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: integer
    """
    try:
        event_form = event_schema.load(request.json)  # type: ignore
    except ValidationError as e:
        raise AppError(str(e.messages)) from e

    event = Event(**event_form, user_id=current_user.id)
    event_id = event_service.save(event)
    db.session.commit()

    return jsonify(id=event_id)


@app.post('/api/event/delete')
@login_required
def delete_event() -> Response:
    """
    ---
    post:
      summary: Delete event.
      tags: [event]
      x-swagger-router-controller: timetable.views.event
      operationId: delete_event
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/EventId'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: integer
    """
    try:
        row = event_id_schema.load(request.json)  # type: ignore
    except ValidationError as e:
        raise AppError(str(e.messages)) from e

    row_id = row.id
    db.session.delete(row)
    db.session.commit()
    return jsonify(id=row_id)
