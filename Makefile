default: web

dev:
	./ve pip install -r requirements.txt -r requirements-dev.txt

web:
	FLASK_APP=timetable FLASK_ENV=development ./ve flask run --port=5001

gen:
	FLASK_APP=timetable ./ve flask gen

test:
	./ve pylint timetable
	./ve mypy timetable
