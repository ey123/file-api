DOCKER_REPO = your_docker_username/your_docker_repo
DOCKER_TAG = latest

.PHONY: test lint build_docker push_docker

default: test lint format

format:
	black -l 79 --target-version py39 tests services app.py

test:
	python -m unittest discover -s tests

lint:
	PYTHONPATH=. pylint --rcfile=.pylintrc --recursive=y tests services

build_docker:
	docker build -t $(DOCKER_REPO):$(DOCKER_TAG) .

push_docker:
	docker push $(DOCKER_REPO):$(DOCKER_TAG)
