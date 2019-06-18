.DEFAULT_GOAL := help
.PHONY: help dev

DEV_API_IMAGE=library-api-dev-img
DEV_DB_IMAGE=library-db-dev-img

DEV_API_CONTAINER=library_api_dev
DEV_DB_CONTAINER=library_db_dev

PROD_API_IMAGE=library-api-prod-img
PROD_DB_IMAGE=library-db-prod-img

PROD_API_CONTAINER=library_api_prod
PROD_DB_CONTAINER=library_db_prod

DB_USER=dev
DB_PASS=dev_secret
DB_NAME=library

dev: dev-run dev-provision ## Create dev environment

dev-images: ## Make dev container images
	docker build -t $(DEV_API_IMAGE) --target dev -f ./env/containers/api/Dockerfile  .
	docker build -t $(DEV_DB_IMAGE) --target dev -f ./env/containers/db/Dockerfile  .

dev-run: dev-run-db dev-run-api

dev-run-db: # TODO: fix sleep 5
	docker run -e POSTGRES_USER=$(DB_USER) -e POSTGRES_PASSWORD=$(DB_PASS) -e POSTGRES_DB=$(DB_NAME) -p 5432:5432 --name $(DEV_DB_CONTAINER) -d $(DEV_DB_IMAGE)
	sleep 5

dev-run-api:
	$(eval $@_DB_HOST := $(shell docker inspect --format '{{ .NetworkSettings.IPAddress }}' $(DEV_DB_CONTAINER)))
	docker run -e DEBUG=TRUE -e DB_HOST=$($@_DB_HOST) -e DB_USER=$(DB_USER) -e DB_PASSWORD=$(DB_PASS) -e DB_NAME=$(DB_NAME) -p 3000:8080 -v $(shell pwd):/usr/src/app/ --name $(DEV_API_CONTAINER) -d $(DEV_API_IMAGE)

dev-provision:
	$(eval $@_DB_HOST := $(shell docker inspect --format '{{ .NetworkSettings.IPAddress }}' $(DEV_DB_CONTAINER)))
	docker exec -e DB_HOST=$($@_DB_HOST) -e DB_USER=$(DB_USER) -e DB_PASSWORD=$(DB_PASS) -e DB_NAME=$(DB_NAME) -it $(DEV_API_CONTAINER) /bin/bash -c "python library/manage.py migrate"

dev-clean: ## Tear down dev env
	- docker kill $(DEV_API_CONTAINER) $(DEV_DB_CONTAINER)
	- docker rm $(DEV_API_CONTAINER) $(DEV_DB_CONTAINER)

dev-clean-images: dev-clean ## Remove dev docker images
	docker rmi $(DEV_DB_IMAGE) $(DEV_API_IMAGE)

prod-images: ## Make prod container images
	docker build -t $(PROD_API_IMAGE) --target prod -f ./env/containers/api/Dockerfile .
	docker build -t $(PROD_DB_IMAGE) --target prod -f ./env/containers/db/Dockerfile .

prod: prod-run-db prod-run-api ## Run prod environment

prod-run-db: # TODO: fix sleep 5
	docker run -e POSTGRES_USER=$(DB_USER) -e POSTGRES_PASSWORD=$(DB_PASS) -e POSTGRES_DB=$(DB_NAME) -p 5432:5432 --name $(PROD_DB_CONTAINER) -d $(PROD_DB_IMAGE)
	sleep 5

prod-run-api:
	$(eval $@_DB_HOST := $(shell docker inspect --format '{{ .NetworkSettings.IPAddress }}' $(PROD_DB_CONTAINER)))
	docker run -e DB_HOST=$($@_DB_HOST) -e DB_USER=$(DB_USER) -e DB_PASSWORD=$(DB_PASS) -e DB_NAME=$(DB_NAME) -p 80:8080 --name $(PROD_API_CONTAINER) -d $(PROD_API_IMAGE)

test: ## Run the tests in local dev env
	$(eval $@_DB_HOST := $(shell docker inspect --format '{{ .NetworkSettings.IPAddress }}' $(DEV_DB_CONTAINER)))
	docker exec -e DB_HOST=$($@_DB_HOST) -e DB_USER=$(DB_USER) -e DB_PASSWORD=$(DB_PASS) -e DB_NAME=$(DB_NAME) -it $(DEV_API_CONTAINER) /bin/bash -c "coverage run --source='.' library/manage.py test library && coverage report"

lint: ## Lint code using black, isort, flake8
	docker exec -it $(DEV_API_CONTAINER) /bin/bash -c "black ."
	docker exec -it $(DEV_API_CONTAINER) /bin/bash -c "isort -rc ."
	docker exec -it $(DEV_API_CONTAINER) /bin/bash -c "flake8 ."

exec: ## Exec into api container
	docker exec -it $(DEV_API_CONTAINER) bash

shell: ## Exec into django shell
	docker exec -it $(DEV_API_CONTAINER) /bin/bash -c "python library/manage.py shell"

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
