#!/bin/bash
cd ..
docker-compose up -d db
docker-compose up -d memcached
docker-compose build web
docker-compose up migrate
docker-compose up loaddata
docker-compose up web
