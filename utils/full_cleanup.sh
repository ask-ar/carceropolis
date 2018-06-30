#!/bin/bash

docker-compose down --rmi all -v --remove-orphans
docker container ls -a | grep carceropolis | awk '{print $1}' | xargs docker container rm -f -l -v
docker image ls -a | grep carceropolis | awk '{print $1}' | xargs docker image rm -f
docker image prune
docker volume prune

echo -n "Do you want to remove keep this git repo clean as new (y/n)? "
old_stty_cfg=$(stty -g)
stty raw -echo
answer=$( while ! head -c 1 | grep -i '[ny]' ;do true ;done )
stty $old_stty_cfg
if echo "$answer" | grep -iq "^y" ;then
    echo "You choose to do a git cleanup here. Running 'git clean -df'"
    git clean -df
else
    echo No, skipping this step!
fi
