from flask import redirect, url_for

from timetable import app

@app.route('/')
def index():
    return redirect(url_for('event_index'))
