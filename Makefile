install:
	poetry install

dev:
	poetry run flask run

test:
	poetry run ruff check --fix timetable
	poetry run mypy timetable
