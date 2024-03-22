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
    return CategoryResponse(categories=CATEGORIES).model_dump(mode='json')


@app.get('/api/event/list')
@login_required
def get_event_list() -> dict:
    form = EventListRequest(**request.args)
    events = event_svc.get_event_list(current_user.id, form.start, form.end)
    return EventListResponse(events=events).model_dump(mode='json', by_alias=True)


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
    return form.model_dump(mode='json')
