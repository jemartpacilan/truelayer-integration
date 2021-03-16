install:
	@pipenv install --dev

test:
	@pipenv install --dev
	pipenv run pytest

run:
	@FLASK_APP=app/routes.py pipenv run flask run


lint:
	@pipenv run flake8

.PHONY: install run lint
