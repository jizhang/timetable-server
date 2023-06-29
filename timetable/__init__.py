from typing import Optional

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('timetable.default_settings')
app.config.from_envvar('TIMETABLE_SETTINGS', silent=True)

db = SQLAlchemy(app)

# Configure login
login_manager = LoginManager(app)

from timetable.models.user import User
from timetable.services import user as user_svc


@login_manager.user_loader
def load_user(user_id: str) -> Optional[User]:
    return user_svc.get_user(user_id)


class AppError(Exception):
    def __init__(self, message: str, code=400):
        super().__init__(message)
        self.message = message
        self.code = code


import timetable.commands
import timetable.views
