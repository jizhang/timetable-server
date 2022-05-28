default: web

dev:
	pip install -r requirements.txt -r requirements-dev.txt

web:
	flask run

gen:
	flask gen

test:
	pylint timetable
	mypy timetable
