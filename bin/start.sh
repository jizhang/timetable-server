#!/bin/bash

export FLASK_APP=timetable
export FLASK_DEBUG=1
export TIMETABLE_SETTINGS=../application.cfg
flask run
