docker-compose exec carceropolis sh -c "python manage.py dumpdata --natural-foreign -e sessions -e admin -e contenttypes -e auth.Permission > carceropolis/fixtures/initialdata.json"
docker-compose exec carceropolis sh -c "bzip2 -9 -f carceropolis/fixtures/initialdata.json"
