from flask import request
from flask_login import login_user
from werkzeug.security import check_password_hash

from timetable import AppError, app
from timetable.services import user as user_svc

from .models.user import CurrentUser, LoginForm


@app.post('/api/user/login')
def user_login() -> dict:
    form = LoginForm.model_validate(request.json)
    user = user_svc.get_by_username(form.username)
    if user is None:
        raise AppError('Username not found')

    if not check_password_hash(user.password, form.password):
        raise AppError('Invalid password')

    login_user(user, remember=True)

    resp = CurrentUser.model_validate(user, from_attributes=True)
    return resp.model_dump()
