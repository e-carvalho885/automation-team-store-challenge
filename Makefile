SHELL := /bin/bash # Use bash syntax
ARG := $(word 2, $(MAKECMDGOALS) )


docker_build:
	docker-compose up -d --build

docker_up:
	docker-compose up -d

docker_up_single:
	docker-compose up -d api 

docker_stop:
	docker-compose stop

docker_update_dependencies:
	docker-compose down
	docker-compose up -d --build --remove-orphans

docker_test:
	docker-compose run api python manage.py test $(ARG) --parallel --keepdb

docker_create_admin_user:
	docker-compose exec api python manage.py createsuperuser

docker_makemigrations:
	docker-compose exec api python manage.py makemigrations

docker_logs:
	docker-compose logs -f $(ARG)

docker_migrate:
	docker-compose exec api python manage.py migrate

test:
	python3 manage.py test $(ARG) --parallel --keepdb


