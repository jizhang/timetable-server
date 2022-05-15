from typing import Any

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config.from_object('timetable.default_settings')
app.config.from_envvar('TIMETABLE_SETTINGS', silent=True)

db: Any = SQLAlchemy(app)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    password_hash = app.config['USERS'].get(username)
    if password_hash is not None:
        return check_password_hash(password_hash, password)
    return False


class AppError(Exception):
    status_code = 400


# pylint: disable=cyclic-import,wrong-import-position
import timetable.views
import timetable.commands.spec
