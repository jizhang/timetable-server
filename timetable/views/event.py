import datetime

from flask import request, jsonify, Response
from marshmallow import ValidationError

from timetable import app, db, auth, AppError
from timetable.consts import CATEGORIES
from timetable.models.event import Event
from timetable.services import event as event_svc
from timetable.views import InvalidUsage
from timetable.schemas.event import categories_schema, event_schema



@app.get('/api/event/categories')
@auth.login_required
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


@app.post('/api/event/ping')
@auth.login_required
def event_ping():
    return jsonify('pong')


@app.get('/api/event/list')
@auth.login_required
def event_list():
    try:
        start = datetime.datetime.strptime(request.args['start'], '%Y-%m-%d')
        end = datetime.datetime.strptime(request.args['end'], '%Y-%m-%d')
    except Exception:
        raise InvalidUsage('invalid dates')

    rows = db.session.query(Event).\
        filter(Event.start >= start.strftime('%Y-%m-%d 00:00:00')).\
        filter(Event.start <= end.strftime('%Y-%m-%d 23:59:59')).\
        order_by(Event.id).\
        all()

    events = []
    for row in rows:
        events.append({
            'id': row.id,
            'title': row.title,
            'start': row.start.strftime('%Y-%m-%d %H:%M:%S'),
            'end': row.end.strftime('%Y-%m-%d %H:%M:%S'),
            'categoryId': row.category_id,
            'color': get_category_color(row.category_id)
        })


    return jsonify(events)


def get_category_color(category_id):
    for item in CATEGORIES:
        if item['id'] == category_id:
            return item['color']
    return ''


@app.post('/api/event/save')
@auth.login_required
def save_event():
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
          application/x-www-form-urlencoded:
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
        event_form = event_schema.load(request.form)
    except ValidationError as e:
        raise AppError(e.messages)

    event = Event(**event_form)
    event_svc.save(event)
    db.session.commit()

    return jsonify({'id': event.id})


@app.post('/api/event/delete')
@auth.login_required
def event_delete() -> Response:
    if not request.form.get('id'):
        raise AppError('ID cannot be empty.')

    row = db.session.query(Event).get(request.form['id'])
    if row is None:
        raise AppError('Event not found.')

    db.session.delete(row)
    db.session.commit()
    return jsonify('ok')
