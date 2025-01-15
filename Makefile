.PHONY: run lint test build-docker run-docker format install-hooks install-env remove-env lock-env

run:
	pipenv run python src/main.py

lint:
	pipenv run pylint src/

type-check:
	pipenv run mypy src/

lint-all:
	pipenv run pylint src/
	pipenv run mypy src/

test:
	PYTHONPATH=src pipenv run pytest tests/

build-docker:
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