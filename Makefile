COMPOSE_ENV = "local"
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

help:
	@echo "Please use 'make <target>' where <target> is one of the following:"
	@echo "  run                    to build and run the docker containers."
	@echo "  build                  to build the docker image."
	@echo "  up                     to run the docker containers."
	@echo "  logs                   to output (follow) docker logs."
	@echo "  teardown               to teardown the docker containers."
	@echo "  recreate               to teardown and run the docker containers again."


run:
	docker compose up -d --build

build:
	docker compose build

up:
	docker compose up -d

logs:
	docker compose logs -f

teardown:
	docker compose down -v

recreate: teardown run
