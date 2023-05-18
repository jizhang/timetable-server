from flask import Response, jsonify, request
from flask_login import login_user
from werkzeug.security import check_password_hash
from marshmallow import ValidationError

from timetable import app, AppError
from timetable.services import user as user_svc
from timetable.schemas.login_form import login_form_schema
from timetable.schemas.current_user import current_user_schema


@app.post("/api/user/login")
def user_login() -> Response:
    """
    ---
    post:
      summary: User login
      tags: [user]
      x-swagger-router-controller: timetable.views.user.index
      operationId: user_login
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/LoginForm'
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CurrentUser'
    """
    if not isinstance(request.json, dict):
        raise AppError("Invalid request body")

    try:
        form = login_form_schema.load(request.json)
    except ValidationError as e:
        raise AppError(str(e.messages))

    user = user_svc.get_by_username(form["username"])
    if user is None:
        raise AppError("Username not found")

    if not check_password_hash(user.password, form["password"]):
        raise AppError("Invalid password")

    login_user(user, remember=True)
    return jsonify(current_user_schema.dump(user))
