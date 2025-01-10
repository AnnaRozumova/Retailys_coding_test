.PHONY: run lint test coverage-report build format install-hooks install-env remove-env lock-env

run:
	pipenv run python src/main.py

lint:
	pipenv run pylint src/

test:
	pipenv run pytest --cov=src --cov-config=.coveragerc --cov-report=term --cov-report=html tests/

coverage-report:
	xdg-open htmlcov/index.html || open htmlcov/index.html

build:
	docker build -t xml-webapp .

run-docker:
	docker run -p 5000:5000 xml-webapp

install-env:
	PIPENV_VENV_IN_PROJECT=1 pipenv install --dev

lock-env:
	pipenv lock

remove-env:
	pipenv --rm || echo "Environment not found"

install-hooks:
	pipenv run pre-commit install