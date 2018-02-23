#!/bin/bash

docker-compose down --rmi all -v --remove-orphans
docker container ls -a | grep carceropolis | awk '{print $1}' | xargs docker container rm -f -l -v
docker image ls -a | grep carceropolis | awk '{print $1}' | xargs docker image rm -f
docker image prune
docker volume prune
