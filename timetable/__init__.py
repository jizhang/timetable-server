# -*- coding: utf-8 -*-

from flask import Flask
app = Flask(__name__)
app.config.from_object('timetable.default_settings')
app.config.from_envvar('TIMETABLE_SETTINGS', silent=True)

import timetable.views
