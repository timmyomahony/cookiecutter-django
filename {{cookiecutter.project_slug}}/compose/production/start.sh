#!/usr/bin/env bash
cd /home/admin/{{cookiecutter.project_slug}}/
docker-compose -f production.yml build
docker-compose -f production.yml run django python manage.py migrate
docker-compose -f production.yml run django python manage.py collectstatic --noinput

docker-compose -f production.yml down
docker-compose -f production.yml up
