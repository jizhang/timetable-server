from flask import Response, jsonify, request
from flask_login import current_user, login_required

from timetable import app, db
from timetable.consts import CATEGORIES
from timetable.models.event import Event
from timetable.services import event as event_svc

from .models.event import CategoryResponse, EventForm, EventId, EventListRequest, EventListResponse


@app.get('/api/event/categories')
@login_required
def get_event_categories() -> dict:
    return CategoryResponse(categories=CATEGORIES).model_dump()


@app.get('/api/event/list')
@login_required
def get_event_list() -> Response:
    form = EventListRequest(**request.args)
    events = event_svc.get_event_list(current_user.id, form.start, form.end)
    resp = EventListResponse(events=events).model_dump_json(by_alias=True)
    return Response(resp, mimetype='application/json')


@app.post('/api/event/save')
@login_required
def save_event() -> Response:
    form = EventForm.model_validate(request.json)
    event = Event(**dict(form), user_id=current_user.id)
    event_id = event_svc.save(event)
    db.session.commit()
    return jsonify(id=event_id)


@app.post('/api/event/delete')
@login_required
def delete_event() -> dict:
    form = EventId.model_validate(request.json)
    event_svc.delete_event(form.id)
    db.session.commit()
    return form.model_dump()
