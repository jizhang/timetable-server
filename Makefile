default: web

dev:
	poetry install
	poetry run pre-commit install

web:
	poetry run flask run

gen:
	poetry run flask gen

test:
	poetry run pylint timetable
	poetry run mypy timetable
