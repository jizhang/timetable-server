call C:\ProgramData\Anaconda3\Scripts\activate timetable

set FLASK_APP=timetable
set FLASK_ENV=development
set FLASK_RUN_HOST=0.0.0.0
set FLASK_RUN_PORT=5001
flask %*
