# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('timetable.default_settings')
app.config.from_envvar('TIMETABLE_SETTINGS', silent=True)

db = SQLAlchemy(app)


import timetable.views
