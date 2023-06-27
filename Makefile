default: web

dev:
	poetry install

web:
	poetry run flask run

gen:
	poetry run flask gen

test:
	poetry run ruff timetable
	poetry run mypy timetable

prod:
	poetry install --extras gunicorn --without dev
